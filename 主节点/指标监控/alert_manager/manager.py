# encoding: utf-8
"""
@author: The King
@project: KafkaDistributedCrawler
@file: manager.py
@time: 2024/8/7 19:41
"""

from kafka import KafkaConsumer
import json
import redis
import smtplib
from email.mime.text import MIMEText

# Kafka consumer for alerts
consumer = KafkaConsumer(
    'alerts',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def send_email_alert(subject, message):
    # Configure email settings
    sender = 'your_email@example.com'
    recipients = ['recipient@example.com']
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    # Send email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.sendmail(sender, recipients, msg.as_string())
        print("Email alert sent successfully")
    except Exception as e:
        print(f"Failed to send email alert: {e}")


def handle_alert(alert):
    print(f"Received alert: {alert}")
    if alert['type'] == 'anti_scraping_alert':
        send_email_alert("Anti-Scraping Alert", alert['message'])
        redis_client.set('scraping_status', 'paused')
        # Additional handling code, such as logging or taking automated actions


def check_system_health():
    while True:
        health_status = redis_client.get('system_health')
        if health_status != b'healthy':
            send_email_alert("System Health Alert", "System health is not healthy!")
        time.sleep(60)


for message in consumer:
    alert = message.value
    handle_alert(alert)
