import chromadb
from chromadb.config import Settings
from src.dao.IDao import IDao


class EmbeddingDao(IDao):
    def __init__(self, collection_name="text_embeddings"):
        """
        Inizializza la connessione a ChromaDB e crea la collezione se non esiste.
        """
        self.client = chromadb.Client(Settings())
        self.collection_name = collection_name
        self.collection = self.get_or_create_collection()

    def get_or_create_collection(self):
        """
        Recupera la collezione esistente o ne crea una nuova se non esiste.
        """
        existing_collections = self.client.list_collections()
        if self.collection_name in [col.name for col in existing_collections]:
            return self.client.get_collection(name=self.collection_name)
        else:
            return self.client.create_collection(name=self.collection_name)

    def save(self, documents, embeddings, metadatas=None, ids=None):
        """
        Salva i documenti e gli embedding nel VectorDB.

        Args:
        - documents (list of str): Lista di testi/documenti.
        - embeddings (list of list of floats): Lista di embedding corrispondenti ai documenti.
        - metadatas (list of dict, optional): Lista di dizionari con metadati per ogni documento.
        - ids (list of str, optional): Lista di ID univoci per ogni documento.
        """
        self.collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

    def query(self, query_texts, n_results=10, where=None, where_document=None):
        """
        Esegue una query nel VectorDB per trovare i documenti più simili.

        Args:
        - query_texts (list of str): Lista di testi di query.
        - n_results (int, optional): Numero di risultati da restituire. Default è 10.
        - where (dict, optional): Filtro per i metadati.
        - where_document (dict, optional): Filtro per il contenuto del documento.

        Returns:
        - results: I risultati della query, contenenti i documenti più simili.
        """
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document
        )
        return results
