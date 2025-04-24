import json
import time
import logging
from kafka import KafkaConsumer
import mysql.connector
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_HOST = "mysql"  # Use 'localhost' if running locally, or 'mysql' in Docker
DB_NAME = "logs_db"
DB_USER = "log_user"
DB_PASS = "log_pass"
DB_PORT = "3306"

# Kafka configuration
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPICS = ["api_logs", "error_logs", "performance_logs"]
CONSUMER_GROUP = "log_processor"

def connect_to_kafka(broker, topics, group_id):
    """Establish connection to Kafka with retry logic"""
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=[broker],
                group_id=group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: x.decode('utf-8')
            )
            logger.info(f"Connected to Kafka, listening on topics: {topics}")
            return consumer
        except Exception as e:
            logger.error(f"Kafka connection error: {e}")
            retry_count += 1
            time.sleep(min(retry_count * 2, 30))
    
    raise Exception("Kafka connection failed after max retries")

def connect_to_database():
    """Connect to MySQL database with retries"""
    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            logger.info("Connected to MySQL database")
            return conn
        except Exception as e:
            logger.error(f"MySQL connection error: {e}")
            retry_count += 1
            time.sleep(min(retry_count * 2, 30))
    
    raise Exception("MySQL connection failed after max retries")

def setup_database(conn):
    """Create tables in MySQL if they don't exist"""
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        method VARCHAR(10),
        endpoint VARCHAR(255),
        status_code INT,
        response_time_ms FLOAT,
        client_ip VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS errors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        method VARCHAR(10),
        endpoint VARCHAR(255),
        status_code INT,
        error_message TEXT,
        stack_trace TEXT,
        client_ip VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        endpoint VARCHAR(255),
        response_time_p99 FLOAT,
        response_time_avg FLOAT,
        request_count INT,
        error_rate FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    logger.info("MySQL tables ensured")

def process_log(log_data, conn, topic):
    """Parse log JSON and insert into appropriate table"""
    try:
        data = json.loads(log_data)
        timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
        cursor = conn.cursor()

        if topic == "performance_logs":
            cursor.execute("""
            INSERT INTO performance_metrics (timestamp, endpoint, response_time_p99, response_time_avg, request_count, error_rate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                timestamp,
                data.get('endpoint', ''),
                data.get('response_time_ms', 0.0),
                data.get('response_time_ms', 0.0),
                1,  # Placeholder for count
                1.0 if data.get('status_code', 200) >= 400 else 0.0
            ))

        elif topic == "error_logs":
            status_code = data.get('status_code', 0)
            if status_code >= 400:
                cursor.execute("""
                INSERT INTO errors (timestamp, method, endpoint, status_code, error_message, stack_trace, client_ip)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    timestamp,
                    data.get('method', 'UNKNOWN'),
                    data.get('endpoint', ''),
                    status_code,
                    data.get('error_message', ''),
                    data.get('stack_trace', ''),
                    data.get('client_ip', '')
                ))

        elif topic == "api_logs":
            cursor.execute("""
            INSERT INTO requests (timestamp, method, endpoint, status_code, response_time_ms, client_ip)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                timestamp,
                data.get('method', 'UNKNOWN'),
                data.get('endpoint', ''),
                data.get('status_code', 0),
                data.get('response_time_ms', 0.0),
                data.get('client_ip', '')
            ))

        conn.commit()
        cursor.close()
        logger.debug(f"Log from topic '{topic}' processed: {data.get('endpoint', '')}")

    except Exception as e:
        logger.error(f"Log processing error for topic '{topic}': {e}")
        conn.rollback()

def main():
    try:
        conn = connect_to_database()
        setup_database(conn)
        consumer = connect_to_kafka(KAFKA_BROKER, KAFKA_TOPICS, CONSUMER_GROUP)

        logger.info("Starting log consumption...")
        for message in consumer:
            process_log(message.value, conn, message.topic)

    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()
        if 'conn' in locals():
            conn.close()
        logger.info("Shutdown complete")

if __name__ == "__main__":
    main()
