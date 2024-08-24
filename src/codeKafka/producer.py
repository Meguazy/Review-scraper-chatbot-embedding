from kafka import KafkaProducer

from scraper.IndeedScraper import IndeedScraper

import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],  # Ensure Kafka is running on this address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def main():
    scraper = IndeedScraper(producer)
    try:
        while True:
            url = input("Enter the URL to scrape: ")
            scraper.scrape_and_publish(url)
    except KeyboardInterrupt:
        logger.info("Scraper interrupted by user")
    finally:
        producer.close()  # Close Kafka producer on exit
        logger.info("Kafka producer closed")

if __name__ == "__main__":
    main()
