from kafka import KafkaProducer
import logging

def send_to_consumer(topic_name: str, data: dict, producer: KafkaProducer, logger: logging.Logger):
    try:
        producer.send(topic_name, data)
        producer.flush()
        logger.info(f"Sent data to Kafka topic '{topic_name}': {data}")
    except Exception as e:
        logger.error(f"Failed to send data to Kafka: {e}")