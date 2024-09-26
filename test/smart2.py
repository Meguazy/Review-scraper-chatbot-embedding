from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, WebDriverException
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_website(url):
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

    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    return page_source

from bs4 import BeautifulSoup

def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    cleaned_text = soup.get_text("\n", strip=True)
    return cleaned_text

from langchain_ollama.llms import OllamaLLM
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

MODEL_NAME = "mistral"

def parse_with_olama(dom_chunks, parse_description):
    # Instantiate the OllamaLLM with the model name as a string
    llama = OllamaLLM(model=MODEL_NAME) if MODEL_NAME else None

    ITfirm_template = """
    I want you to act as a consultant for a new IT firm.
    Return a list of firm names and a locality which is suitable for such a firm in India. The name should be catchy and the locality should yield profit.
    What are some good names and respective area for IT firm that does {firm_description}
    """

    prompt_template = PromptTemplate(
        input_variables=["firm_description"],
        template=ITfirm_template,
    )

    description = "It is software dev firm specifically focusing on automation software"

    prompt_template.format(firm_description=description)

    chain = LLMChain(llm=llama, prompt=prompt_template)
    print(chain.run())


if __name__ == "__main__":
    url = "https://www.indeed.com/cmp/Fastweb/reviews?fcountry=IT&lang=it"
    page_source = scrape_website(url)
    body_content = extract_body_content(page_source)
    cleaned_text = clean_content(body_content)
    print(cleaned_text)
    # Example usage
    parse_description = "List me the reviews with review title, review body and review score."
    dom_chunks = [cleaned_text[i:i+6000] for i in range(0, len(cleaned_text), 6000)]
    parsed_results = parse_with_olama(cleaned_text, parse_description)
    print(parsed_results)
