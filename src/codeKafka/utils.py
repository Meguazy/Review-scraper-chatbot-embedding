import hashlib
import logging

from kafka import KafkaProducer

def send_to_consumer(topic_name: str, data: dict, producer: KafkaProducer, logger: logging.Logger):
    try:
        producer.send(topic_name, data)
        producer.flush()
        logger.info(f"Sent data to Kafka topic '{topic_name}': {data}")
    except Exception as e:
        logger.error(f"Failed to send data to Kafka: {e}")



def generate_id_from_text(text):
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    
    # Update the hash object with the text encoded to bytes
    hash_object.update(text.encode('utf-8'))
    
    # Get the hexadecimal representation of the hash
    return hash_object.hexdigest()