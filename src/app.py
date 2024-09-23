import streamlit as st
import os
import json
import logging
from kafka import KafkaProducer
from scraper.IndeedScraper import IndeedScraper
from dao.EmbeddingDao import EmbeddingDao
from embedding.embedder import TextEmbedder
from embedding.text_generation import TextGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the Hugging Face API key
HUGGINFACE_API_KEY = os.environ.get('HUGGINFACE_API_KEY')

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['host.docker.internal:9093'],  # Ensure Kafka is running on this address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize the objects
textEmbedder = TextEmbedder()
embedding_dao = EmbeddingDao()
generator = TextGenerator(model_name="mistralai/Mistral-Nemo-Instruct-2407", api_key=HUGGINFACE_API_KEY)

# Get or create the collection for embedding queries
collection = embedding_dao.get_or_create_collection("reviews")

def clean_reviews(query_results):
    """
    Cleans the reviews from the query results.
    """
    for result in query_results['documents']:
        # Remove newline characters from each review
        cleaned_reviews = [item.replace('\n', ' ') for item in result]
    joined_reviews = "\n".join([f"- Recensione {i+1}: \"{review}\"" for i, review in enumerate(cleaned_reviews)])
    return joined_reviews

# Streamlit UI
st.title("Web Scraping and Chatbot Interface")

# Create a session state to handle the execution state
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# First text box and button for scraping
st.header("URL Scraper")
url_input = st.text_input("Enter the URL to scrape (For example: https://www.indeed.com/cmp/Fastweb/)")
scrape_button = st.button("Scrape and Publish", disabled=st.session_state.is_running)

if scrape_button:
    st.session_state.is_running = True  # Block both buttons
    if url_input:
        scraper = IndeedScraper(producer)
        with st.spinner('Scraping and publishing...'):
            try:
                scraper.scrape_and_publish(url_input)
                st.success("Data scraped and published to Kafka successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL.")
    st.session_state.is_running = False  # Unblock both buttons

# Second text box and button for chatbot interaction
st.header("Chatbot Interaction")
query_input = st.text_input("Enter your query")
company_name_input = st.text_input("Enter company name to filter by")
n_results_input = st.number_input("Enter the number of results", min_value=1, value=5)
chatbot_button = st.button("Ask Chatbot", disabled=st.session_state.is_running)

if chatbot_button:
    st.session_state.is_running = True  # Block both buttons
    if query_input:
        with st.spinner('Processing your query...'):
            try:
                # Query the collection
                query_results = textEmbedder.query_db(query_input, collection, company_name=company_name_input, n_results=n_results_input)

                # Clean and prepare reviews for the prompt
                reviews = clean_reviews(query_results)
                
                # Construct the prompt
                prompt = generator.build_prompt(query_input, context=reviews, type="long", company_name=company_name_input)
                st.write("### Prompt")
                st.write(prompt)

                # Generate text based on the prompt
                generated_text = generator.text_generation(prompt)
                st.write("### Chatbot Response")
                st.write(generated_text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
    st.session_state.is_running = False  # Unblock both buttons
