# producer.py
from kafka import KafkaProducer
from datetime import datetime
import json
# --------- import necessary modules -------
# Store data as a csv file written out
from csv import writer
import pandas as pd

from selenium import webdriver
# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service as ChromeService
# Manages Binaries needed for WebDriver without installing anything directly
from webdriver_manager.chrome import ChromeDriverManager
# Allows searchs similar to beautiful soup: find_all
from selenium.webdriver.common.by import By
# Locate elements on page and throw error if they do not exist
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException

import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class IndeedScraper():
    def __init__(self):
        # Allows you to cusotmize: ingonito mode, maximize window size, headless browser, disable certain features, etc
        option= webdriver.ChromeOptions()
        # Going undercover:
        option.add_argument("--incognito")
        # Define the driver to use
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
    
    def scrape_and_publish(self, url):
        url_to_format = url + "reviews/?fcountry=ALL&start={}"

        try:
            # Finding total number of reviews to understand how many times we have to loop the program. 
            self.driver.get(url_to_format.format(0))
            # 'div.css-104u4ae.eu4oa1w0' contains the number of reviews. 
            tot_reviews = self.driver.find_element(By.CSS_SELECTOR, "div.css-104u4ae.eu4oa1w0").text
            print(self.driver.find_element(By.CSS_SELECTOR, "span.css-1cxc9zk.e1wnkr790").text.split("\n")[-1])
            # If the reviews are more than 1000 there is a K at the end, so we substitute it.
            num_tot_reviews = int(float(str(tot_reviews).replace("K", "")) * 1000) if "K" in tot_reviews else int(tot_reviews)

            for i in range(0, num_tot_reviews, 20):
                print(url_to_format.format(i))
                self.driver.get(url_to_format.format(i))

                reviews = self.driver.find_elements(By.CSS_SELECTOR, "div.css-lw17hn.eu4oa1w0")

                bottom_range = 0 if i == 0 else 1

                for j in range(bottom_range, len(reviews)):
                    review = reviews[j]
                    review_title = review.find_element(By.CSS_SELECTOR, "h2.css-1edqxdo.e1tiznh50")
                    review_body = review.find_element(By.CSS_SELECTOR, "div.css-hxk5yu.eu4oa1w0")
                    review_score = review.find_element(By.CSS_SELECTOR, "button.css-1c33izo.e1wnkr790")

                    review_dict = {'company_name': str(url).split('/')[-2], 'review_title': review_title.text, 'review_body': review_body.text, 'review_score': review_score.text}
                    send_to_consumer('reviews', review_dict)

        except NoSuchElementException:
            print("The page you were trying to scrape doesn't exist")
        except InvalidArgumentException:
            print("Invalid argument")
    
def send_to_consumer(topic_name: str, data: dict):
    producer.send(topic_name, data)

scraper = IndeedScraper()

while True:
    url = input("Inserisci l'url di cui fare scraping: ")
    scraper.scrape_and_publish(url)