# encoding: utf-8
"""
@author: The King
@project: KafkaDistributedCrawler
@file: 主节点接收任务.py
@time: 2024/8/6 17:26
"""

from flask import Flask, request, jsonify
from kafka import KafkaProducer
import redis

app = Flask(__name__)

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='kafka-broker:9092')

# Redis Client
redis_client = redis.StrictRedis(host='redis-server', port=6379, db=0)


@app.route('/api/start-task', methods=['POST'])
def start_task():
    data = request.json
    task_id = data['taskId']
    task_data = data['taskData']

    # 创建 Kafka Topic
    create_kafka_topic(task_id)

    # 写入 Kafka
    producer.send(task_id, value=task_data.encode('utf-8'))
    producer.flush()

    # 在 Redis 中创建键值对
    redis_client.set(task_id, 'initialized')

    # 根据前端用户操作启动对应子节点
    start_sub_node(task_id)

    return jsonify({'status': 'Task started successfully'})


def create_kafka_topic(topic_name):
    # 使用 Kafka Admin 客户端创建 Topic
    from kafka.admin import KafkaAdminClient, NewTopic
    admin_client = KafkaAdminClient(bootstrap_servers='kafka-broker:9092', client_id='admin-client')
    topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)


def start_sub_node(task_id):
    # 启动子节点（假设通过 Docker API 启动）
    import docker
    client = docker.from_env()
    client.containers.run('my_crawler_image', detach=True, environment={"TASK_ID": task_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
