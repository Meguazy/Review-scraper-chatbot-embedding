from dao.EmbeddingDao import EmbeddingDao
from huggingface_hub import InferenceClient
from embedding.embedder import TextEmbedder

textEmbedder = TextEmbedder()
embedding_dao = EmbeddingDao()
collection = embedding_dao.get_or_create_collection("reviews")

API_KEY = """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"""
client = InferenceClient(token=API_KEY)

if __name__ == "__main__":
    while True:        
        # Query the collection
        query_text = input("Enter your query: ")
        company_name = input("Enter company name to filter by (or press Enter to skip): ")

        results = textEmbedder.query_db(query_text, collection, company_name=company_name, n_results=5)

        # Print results
        cleaned_reviews = None
        print("Query results:")
        for result in results['documents']:
            # Remove newline characters from each review
            cleaned_reviews = [item.replace('\n', ' ') for item in result]
        
        # Join the cleaned reviews into a single string with enumeration and newline characters
        joined_reviews = "\n".join([f"- Recensione {i+1}: \"{review}\"" for i, review in enumerate(cleaned_reviews)])
        
        # Construct the prompt with context
        prompt = f"Recensioni dell'azienda chiamata Fastweb:\n{joined_reviews}\nLa domanda è: {query_text} \n rispondi in modo dettagliato, tenendo conto delle recensioni. La tua risposta deve essere di massimo 50 parole, non ignorare questa istruzione."
        print("-------------PROMPT VALUE-------------")
        print(f"{prompt}")

        result = client.text_generation(prompt, model="mistralai/Mistral-Nemo-Instruct-2407", return_full_text=False)
        print("-------------Response for the text generation model-------------")
        print(f"{result}")
