from chromadb import Collection
from sentence_transformers import SentenceTransformer
from dao.EmbeddingDao import EmbeddingDao

class TextEmbedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextEmbedder, cls).__new__(cls)
            cls._instance.embedding_model = None
            cls._instance.embedding_dao = EmbeddingDao()
        return cls._instance

    def load_model(self, model_name):
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer(model_name)

    def embed(self, text):
        if self.embedding_model is None:
            raise ValueError("Model is not loaded. Call load_model() first.")
        embeddings = self.embedding_model.encode(text)
        return embeddings.tolist()

    def query_db(self, query_text, collection: Collection, n_results=5, company_name=None):
        """
        Queries the ChromaDB collection using the embedding of the query text.

        Args:
        - query_text (str): The text to be queried.
        - collection (Collection): The ChromaDB collection to query.
        - n_results (int): The number of results to return.
        - company_name (str, optional): The company name to filter by.

        Returns:
        - results: The query results from ChromaDB.
        """
        query_embeddings = self.embed(query_text)
        where_clause = self._build_where_clause(company_name)

        results = self.embedding_dao.query(
            query_embeddings=query_embeddings, 
            n_results=n_results, 
            collection=collection,
            where=where_clause
        )
        
        return results

    def _build_where_clause(self, company_name):
        """
        Constructs the where clause for querying the database.

        Args:
        - company_name (str, optional): The company name to filter by.

        Returns:
        - dict or None: The where clause for filtering, or None if no filtering is applied.
        """
        if company_name:
            return {'company_name': company_name}
        return None
