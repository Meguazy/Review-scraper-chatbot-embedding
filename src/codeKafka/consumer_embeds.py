from kafka import KafkaConsumer
from embedding.embedder import TextEmbedder
from dao.EmbeddingDao import EmbeddingDao  # Assicurati che il percorso sia corretto
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

# Loop per processare i messaggi
for message in consumer:
    print("-------------MESSAGE VALUE-------------")
    print(message.value["review_body"])

    # Tokenizza la recensione
    tokens = textEmbedder.tokenize_sentence(message.value["review_body"])
    embeddings = []
    for token in tokens:
        print("-------------TOKENIZATION VALUE-------------")
        print(token)

        # Genera embedding per ogni token
        embedding = textEmbedder.embed(token)
        embeddings.append(embedding)

        print("-------------EMBEDDING VALUE-------------")
        print(embedding)

    # Salva i token e gli embedding nel database (ChromaDB)
    metadatas = [{"source": message.value.get("company_name", "unknown")} for _ in tokens]
    ids = [f"{message.value.get('company_name', 'unknown')}-{i}" for i in range(len(tokens))]

    embedding_dao.save(
        documents=tokens,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
