from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import spacy

class TextEmbedder:
    def __init__(self, model_name='sentence-transformers/multi-qa-MiniLM-L6-cos-v1'):
        """
        Initialize the TextEmbedder with a specified model.
        """
        self.embedding_model = SentenceTransformer(model_name)
        #self.client = chromadb.Client(Settings())
        #self.collection = self.client.create_collection(name="text_embeddings")

        # Load the Italian language model
        self.nlp = spacy.load("it_core_news_sm")

    def tokenize_sentence(self, text):
        """
        Tokenizes the input Italian text into sentences.
        
        Args:
        - text (str): The input Italian text to tokenize.

        Returns:
        - list of str: A list where each element is a sentence from the input text.
        """
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Extract sentences from the processed text
        sentences = [sent.text.strip() for sent in doc.sents]
        
        return sentences

    def embed(self, text):
        """
        Computes the embeddings for the input text using the SentenceTransformer model.
        """
        embeddings = self.embedding_model.encode(text)
        return embeddings

    # def add_to_db(self, text):
    #     """
    #     Adds the text embedding to the ChromaDB collection.
    #     """
    #     embeddings = self.embed(text)
    #     self.collection.add(
    #         documents=[text],
    #         embeddings=[embeddings]
    #     )
    
    def query_db(self, query_text):
        """
        Queries the ChromaDB collection using the embedding of the query text.
        """
        query_embedding = self.embed(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            top_k=5  # Adjust as needed
        )
        return results

# Example usage
if __name__ == "__main__":
    text_embedder = TextEmbedder()
    text = "Questa è una frase di esempio in italiano."
    
    # Add the text to the ChromaDB collection
    text_embedder.add_to_db(text)
    
    # Query the ChromaDB collection
    results = text_embedder.query_db(text)
    print("Query Results:", results)
