from datetime import datetime
from kafka import KafkaConsumer
from embedding.embedder import TextEmbedder
from dao.EmbeddingDao import EmbeddingDao  # Assicurati che il percorso sia corretto
from utils import generate_id_from_text
import json

# Inizializza KafkaConsumer
consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers=['localhost:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Inizializza l'embedder e il DAO per gli embedding
textEmbedder = TextEmbedder()
embedding_dao = EmbeddingDao()

# Get the collection for the embeddings
collection = embedding_dao.get_or_create_collection("reviews")

counter = 0
# Loop per processare i messaggi
for message in consumer:
    unique_id = generate_id_from_text(message.value["review_body"])
    
    # Generate embedding for the review body
    embedding = textEmbedder.embed(message.value["review_body"])

    metadata = {
        'company_name' : message.value.get('company_name', 'unknown'),
        'review_title' : message.value.get('review_title', 'unknown'),
        'review_score' : message.value.get('review_score', 'unknown'),
        'ins_timestamp': datetime.now().isoformat()
    }
    print(metadata)

    # Save the token and embedding in the database (ChromaDB)
    embedding_dao.save(
        documents=[message.value["review_body"]],
        embeddings=[embedding],
        collection=collection,
        metadatas=[metadata],
        ids=[unique_id]
    )

