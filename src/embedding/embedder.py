from chromadb import Collection
from sentence_transformers import SentenceTransformer

from dao.EmbeddingDao import EmbeddingDao
class TextEmbedder:
    def __init__(self, model_name='sentence-transformers/multi-qa-MiniLM-L6-cos-v1'):
        """
        Initialize the TextEmbedder with a specified model.
        """
        self.embedding_model = SentenceTransformer(model_name)
        self.embedding_dao = EmbeddingDao()

    def embed(self, text):
        """
        Computes the embeddings for the input text using the SentenceTransformer model.
        """
        embeddings = self.embedding_model.encode(text)
        return embeddings.tolist()

    def query_db(self, query_text, collection: Collection, n_results = 5, company_name=None):
        """
        Queries the ChromaDB collection using the embedding of the query text and filters by company name.

        Args:
        - query_text (str): The text to be queried.
        - company_name (str, optional): The company name to filter by. If None, no filtering is applied.

        Returns:
        - results: The query results from ChromaDB.
        """
        query_embeddings = self.embed(query_text)
        
        # Create the where clause for metadata filtering
        where_clause = None
        if company_name:
            where_clause = {'company_name': company_name}

        results = self.embedding_dao.query(
            query_embeddings=query_embeddings, 
            n_results=n_results, 
            collection=collection,
            where=where_clause)
        
        return results
