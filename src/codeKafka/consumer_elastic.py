# consumer.py
from kafka import KafkaConsumer
from src.dao.ElasticDao import ElasticDao  # Assicurati che il percorso sia corretto
import json

# Inizializza KafkaConsumer
consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers=['localhost:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Inizializza il DAO per Elasticsearch
elastic_dao = ElasticDao()

# Loop per processare i messaggi
for message in consumer:
    print(message.value)

    # Salva il messaggio raw in Elasticsearch
    elastic_dao.save(document=message.value, id=message.value.get('id'))
