# encoding: utf-8
"""
@author: The King
@project: KafkaDistributedCrawler
@file: resolver.py
@time: 2024/8/7 19:43
"""

import redis
import time

# Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def handle_anti_scraping():
    # Example actions to mitigate anti-scraping measures
    print("Handling anti-scraping measures...")
    time.sleep(10)  # Simulate time taken to handle the issue

    # Actions such as changing IP, updating request headers, etc.
    print("Anti-scraping measures handled successfully.")
    redis_client.set('scraping_status', 'running')


def check_and_resolve_issues():
    while True:
        scraping_status = redis_client.get('scraping_status')
        if scraping_status == b'paused':
            handle_anti_scraping()
        time.sleep(30)  # Check status periodically


if __name__ == "__main__":
    check_and_resolve_issues()
