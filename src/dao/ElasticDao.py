from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

from src.dao.IDao import IDao


class ElasticDao(IDao):
    def __init__(self, index_name="raw_data", kafka_topic='reviews', kafka_servers=['localhost:9093']):
        """Inizializza il DAO per Elasticsearch."""
        self.es = Elasticsearch()
        self.index_name = index_name
        self.consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def connect(self):
        """Connessione Kafka già gestita in __init__."""
        pass

    def save(self, document, id=None):
        """Salva un documento in Elasticsearch."""
        self.es.index(index=self.index_name, id=id, document=document)

    def query(self, query, size=10):
        """Esegue una query su Elasticsearch."""
        results = self.es.search(index=self.index_name, query=query, size=size)
        return results

    def consume_and_save(self):
        """Consuma messaggi da Kafka e li salva in Elasticsearch."""
        for message in self.consumer:
            print("Saving message to Elasticsearch:", message.value)
            self.save(document=message.value)
