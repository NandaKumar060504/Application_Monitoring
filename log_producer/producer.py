import json
import time
import logging
from kafka import KafkaProducer
import socket
import os

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka config from env
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
API_LOGS_TOPIC = os.environ.get('API_LOGS_TOPIC', 'api_logs')
ERROR_LOGS_TOPIC = os.environ.get('ERROR_LOGS_TOPIC', 'error_logs')
PERFORMANCE_LOGS_TOPIC = os.environ.get('PERFORMANCE_LOGS_TOPIC', 'performance_logs')

def connect_kafka():
    """Connect to Kafka with retries"""
    for attempt in range(5):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            logger.info(f"Successfully connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
            return producer
        except Exception as e:
            logger.error(f"Kafka connection failed: {e}, retrying...")
            time.sleep(2)
    raise Exception("Failed to connect to Kafka after retries")

def send_test_log(producer):
    """Send a test log message to Kafka"""
    test_log = {
        "timestamp": "2025-04-08T18:40:00",
        "method": "GET",
        "endpoint": "/api/test",
        "status_code": 500,
        "response_time_ms": 123,
        "client_ip": "127.0.0.1",
        "error_message": "Internal Server Error",
        "stack_trace": "Traceback (most recent call...)"
    }

    producer.send(API_LOGS_TOPIC, key="test", value=test_log)
    producer.send(ERROR_LOGS_TOPIC, key="test", value=test_log)
    producer.send(PERFORMANCE_LOGS_TOPIC, key="test", value=test_log)
    producer.flush()
    logger.info("✅ Test log sent to Kafka!")

if __name__ == "__main__":
    logger.info("Starting Kafka log producer...")
    producer = connect_kafka()
    send_test_log(producer)
