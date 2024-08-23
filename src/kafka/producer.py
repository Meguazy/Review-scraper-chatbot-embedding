from kafka import KafkaProducer
from datetime import datetime
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],  # Ensure Kafka is running on this address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class IndeedScraper():
    def __init__(self):
        option = webdriver.ChromeOptions()
        #option.add_argument("--headless")  # Run in headless mode for efficiency
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")

        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        except WebDriverException as e:
            logger.error(f"Error initializing WebDriver: {e}")
            raise

    def scrape_and_publish(self, url):
        url_to_format = url + "reviews/?fcountry=ALL&start={}"

        try:
            # Getting the number of reviews
            self.driver.get(url_to_format.format(0))

            # Wait for the element to be present
            tot_reviews = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-104u4ae.eu4oa1w0"))
            ).text

            num_tot_reviews = int(float(str(tot_reviews).replace("K", "")) * 1000) if "K" in tot_reviews else int(tot_reviews)

            for i in range(0, num_tot_reviews, 20):
                logger.info(f"Scraping page: {url_to_format.format(i)}")
                self.driver.get(url_to_format.format(i))

                reviews = self.driver.find_elements(By.CSS_SELECTOR, "div.css-lw17hn.eu4oa1w0")

                bottom_range = 0 if i == 0 else 1

                for j in range(bottom_range, len(reviews)):
                    review = reviews[j]
                    review_title = review.find_element(By.CSS_SELECTOR, "h2.css-rv2ti0.e1tiznh50 span.css-15r9gu1.eu4oa1w0").text
                    review_body = review.find_element(By.CSS_SELECTOR, "div.css-hxk5yu.eu4oa1w0").text
                    review_score = review.find_element(By.CSS_SELECTOR, "button.css-szf5tt.e1wnkr790").text

                    review_dict = {
                        'company_name': str(url).split('/')[-2],
                        'review_title': review_title,
                        'review_body': review_body,
                        'review_score': review_score
                    }
                    send_to_consumer('reviews', review_dict)

        except TimeoutException:
            logger.error("Timed out waiting for the element to be present")
        except NoSuchElementException as e:
            logger.error(f"Element not found: {e}")
        except InvalidArgumentException as e:
            logger.error(f"Invalid URL argument: {e}")
        finally:
            self.driver.quit()  # Ensure the browser closes after scraping


def send_to_consumer(topic_name: str, data: dict):
    try:
        producer.send(topic_name, data)
        producer.flush()
        logger.info(f"Sent data to Kafka topic '{topic_name}': {data}")
    except Exception as e:
        logger.error(f"Failed to send data to Kafka: {e}")

def main():
    scraper = IndeedScraper()

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
