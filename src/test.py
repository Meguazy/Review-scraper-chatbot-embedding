import os

from dao.EmbeddingDao import EmbeddingDao
from embedding.embedder import TextEmbedder
from embedding.text_generation import TextGenerator

# Retrieve the secret key from the environment
API_KEY = os.environ.get('API_KEY')

# Initialize the objects
# TextEmbedder is the object that creates the embeddings for the input text
textEmbedder = TextEmbedder()
# EmbeddingDao is the object that interacts with the vector databaseß
embedding_dao = EmbeddingDao()
# TextGenerator is the object that generates text based on the prompt
generator = TextGenerator(model_name="mistralai/Mistral-Nemo-Instruct-2407", api_key=API_KEY)

# Get or create the collection
collection = embedding_dao.get_or_create_collection("reviews")

def clean_reviews(query_results):
    """
    Cleans the reviews from the query results.
    """
    cleaned_reviews = [item.replace('\n', ' ') for item in query_results["documents"][0]]
    joined_reviews = "\n".join([f"- Recensione {i+1}: \"{review}\"" for i, review in enumerate(cleaned_reviews)])
    return joined_reviews

if __name__ == "__main__":
    while True:
        # Query the collection
        query_text = input("Enter your query: ")
        company_name = input("Enter company name to filter by (or press Enter to skip): ")
        query_results = textEmbedder.query_db(query_text, collection, company_name=company_name, n_results=5)

        # Join the cleaned reviews into a single string with enumeration and newline characters
        reviews = clean_reviews(query_results)
        
        # Construct the prompt with context
        prompt = generator.build_prompt(query_text, context=reviews, type="short", company_name=company_name)
        print("-------------PROMPT VALUE-------------")
        print(f"{prompt}")

        # Generate the text based on the prompt
        generated_text = generator.text_generation(prompt)
        print("-------------Response for the text generation model-------------")
        print(f"{generated_text}")
