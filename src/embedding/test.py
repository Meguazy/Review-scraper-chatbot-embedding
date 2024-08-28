from dao.EmbeddingDao import EmbeddingDao
from embedding.T5ItalianGenerator import ItalianTextGenerator
from GPTItalianGenerator import Falcon7BInstructModel
from embedding.embedder import TextEmbedder


textEmbedder = TextEmbedder()
embedding_dao = EmbeddingDao()
italian_generator = Falcon7BInstructModel()
collection = embedding_dao.get_or_create_collection("reviews")


if __name__ == "__main__":
    while True:        
        # Query the collection
        query_text = input("Enter your query: ")
        company_name = input("Enter company name to filter by (or press Enter to skip): ")

        results = textEmbedder.query_db(query_text, collection, company_name=company_name, n_results=2)

        # Print results
        cleaned_reviews = None
        print("Query results:")
        for result in results['documents']:
            # Remove newline characters from each review
            cleaned_reviews = [item.replace('\n', ' ') for item in result]
        
        # Join the cleaned reviews into a single string with enumeration and newline characters
        joined_reviews = "\n".join([f"- Recensione {i+1}: \"{review}\"" for i, review in enumerate(cleaned_reviews)])
        
        # Construct the prompt with context
        prompt = f"Recensioni dell'azienda:\n{joined_reviews}\nDomanda: Considerando le recensioni, {query_text} Rispondi in modo dettagliato."

        print("-------------PROMPT VALUE-------------")
        print(f"Prompt:\n {prompt}")
        # Generate the response
        response = italian_generator.generate_answer(prompt)
        print("-------------RESPONSE VALUE-------------")
        print(f"Response: {response}")


