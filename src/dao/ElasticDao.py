from elasticsearch import Elasticsearch
from dao.IDao import IDao

class ElasticDao(IDao):
    def __init__(self):
        """
        Inizializza la connessione a Elasticsearch e specifica l'indice da usare.
        """
        # Connessione a Elasticsearch in esecuzione su localhost sulla porta 9200
        self.es = Elasticsearch(hosts=["http://elasticsearch:9200"])
        self.index_name = "indice finale"

    def save(self, document, id=None):
        """
        Salva un documento raw in Elasticsearch.

        Args:
        - document (dict): Il documento da salvare.
        - id (str, optional): L'ID del documento. Se non specificato, Elasticsearch genererà un ID univoco.
        """
        response = self.es.index(index=self.index_name, id=id, document=document)
        print(f"Document indexed. ID: {response['_id']}")

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
