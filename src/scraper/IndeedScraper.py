from langdetect import detect, DetectorFactory
from kafka import KafkaProducer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from codeKafka.utils import send_to_consumer

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndeedScraper():
    DetectorFactory.seed = 0
    
    def __init__(self, producer: KafkaProducer):
        self.producer = producer
        
    def initialize_driver(self):
        option = webdriver.ChromeOptions()
        #option.add_argument("--headless")  # Run in headless mode
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--disable-gpu")  # Disable GPU acceleration
        option.add_argument("window-size=1920x1080")  # Set the window size
        option.add_argument("--remote-debugging-port=9222")  # Optional: Enable debugging
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        except WebDriverException as e:
            logger.error(f"Error initializing WebDriver: {e}")
            raise

        return driver

    def scrape_and_publish(self, url):
        driver = self.initialize_driver()
        url_to_format = url + "reviews/?fcountry=ALL&lang=it&start={}"

        try:
            driver.get(url_to_format.format(0))
            # Getting the number of reviews
            # Wait for the element to be present
            tot_reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-104u4ae.eu4oa1w0"))
            ).text

            num_tot_reviews = int(float(str(tot_reviews).replace("K", "")) * 1000) if "K" in tot_reviews else int(tot_reviews)

            for i in range(0, num_tot_reviews, 20):
                logger.info(f"Scraping page: {url_to_format.format(i)}")
                driver.get(url_to_format.format(i))

                # Optionally scroll to load more content
                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                reviews = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-lw17hn.eu4oa1w0"))
                )

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
                    
                    if detect(review_dict['review_body']) == 'it':
                        send_to_consumer('reviews', review_dict, self.producer, logger)

        except TimeoutException:
            logger.error("Timed out waiting for the element to be present")
        except NoSuchElementException as e:
            logger.error(f"Element not found: {e}")
        except InvalidArgumentException as e:
            logger.error(f"Invalid URL argument: {e}")
        finally:
            driver.quit()  # Ensure the browser closes after scraping
