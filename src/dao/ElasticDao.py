from elasticsearch import Elasticsearch
from dao.IDao import IDao


class ElasticDao(IDao):
    def __init__(self, index_name="raw_data"):
        """
        Inizializza la connessione a Elasticsearch e specifica l'indice da usare.
        """
        self.es = Elasticsearch(cloud_id="")
        self.index_name = index_name

    def save(self, document, id=None):
        """
        Salva un documento raw in Elasticsearch.

        Args:
        - document (dict): Il documento da salvare.
        - id (str, optional): L'ID del documento. Se non specificato, Elasticsearch genererà un ID univoco.
        """
        self.es.index(index=self.index_name, id=id, document=document)

    def query(self, query, size=10):
        """
        Esegue una query su Elasticsearch.

        Args:
        - query (dict): La query Elasticsearch in formato JSON.
        - size (int, optional): Il numero di risultati da restituire. Default è 10.

        Returns:
        - results: I risultati della query.
        """
        results = self.es.search(index=self.index_name, query=query, size=size)
        return results
