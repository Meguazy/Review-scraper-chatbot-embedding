from kafka import KafkaConsumer
from dao.ElasticDao import ElasticDao
from dao.SentimentAnalyzer import SentimentAnalyzer
import json

# Inizializza KafkaConsumer
consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers=['kafka:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Inizializza il DAO per Elasticsearch
elastic_dao = ElasticDao()

# Inizializza il SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer()

# Loop per processare i messaggi
for message in consumer:
    document = message.value

    # Estrai il corpo della recensione
    review_body = document.get('review_body', '')

    if review_body:
        # Analizza il sentiment della recensione
        sentiment = sentiment_analyzer.analyze_sentiment(review_body)
        document['sentiment'] = sentiment  # Aggiungi il risultato al documento

    # Salva il documento in Elasticsearch, includendo il sentiment
    elastic_dao.save(document=document, id=document.get('id'))