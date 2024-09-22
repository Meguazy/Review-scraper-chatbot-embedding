import chromadb

from chromadb import Collection
from chromadb.config import Settings
from dao.IDao import IDao


class EmbeddingDao(IDao):
    def __init__(self):
        """
        Inizializza la connessione a ChromaDB.
        """
        # Connect with no authentication
        self.client = chromadb.HttpClient(host='vectordb', port=8000)


    def get_or_create_collection(self, collection_name):
        """
        Recupera la collezione esistente o ne crea una nuova se non esiste.

        Args:
        - collection_name (str): Nome della collezione da recuperare o creare.

        Returns:
        - Collection: La collezione esistente o appena creata.
        """
        existing_collections = self.client.list_collections()
        if collection_name in [col.name for col in existing_collections]:
            return self.client.get_collection(name=collection_name)
        else:
            return self.client.create_collection(name=collection_name)

    def save(self, documents, embeddings, collection: Collection, metadatas=None, ids=None):
        """
        Salva i documenti e gli embedding nella collezione specificata.

        Args:
        - documents (list of str): Lista di testi/documenti.
        - embeddings (list of list of floats): Lista di embedding corrispondenti ai documenti.
        - collection_name (str, optional): Nome della collezione in cui salvare i dati. Default è "text_embeddings".
        - metadatas (list of dict, optional): Lista di dizionari con metadati per ogni documento.
        - ids (list of str, optional): Lista di ID univoci per ogni documento.
        """
        collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

    def query(self, query_embeddings: list, collection: Collection, n_results=10, where=None, where_document=None):
        """
        Esegue una query nel VectorDB per trovare i documenti più simili nella collezione specificata.

        Args:
        - query_texts (list of str): Lista di testi di query.
        - collection_name (str, optional): Nome della collezione da interrogare. Default è "text_embeddings".
        - n_results (int, optional): Numero di risultati da restituire. Default è 10.
        - where (dict, optional): Filtro per i metadati.
        - where_document (dict, optional): Filtro per il contenuto del documento.

        Returns:
        - results: I risultati della query, contenenti i documenti più simili.
        """
        results = collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where,
            where_document=where_document
        )
        return results
