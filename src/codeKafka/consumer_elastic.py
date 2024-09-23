from kafka import KafkaConsumer
from dao.ElasticDao import ElasticDao
from dao.SentimentAnalyzer import SentimentAnalyzer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inizializza KafkaConsumer
consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers=['host.docker.internal:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Inizializza il DAO per Elasticsearch
# docker run -it --network googlescraper_default --rm confluentinc/cp-kafka:latest kafka-console-consumer --bootstrap-server kafka:9092 --topic your_topic --from-beginning
elastic_dao = ElasticDao()

# Inizializza il SentimentAnalyzer 
sentiment_analyzer = SentimentAnalyzer()

print("Consumer started")
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