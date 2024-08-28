from datetime import datetime
from kafka import KafkaConsumer
from embedding.embedder import TextEmbedder
from dao.EmbeddingDao import EmbeddingDao  # Assicurati che il percorso sia corretto
from embedding.GPTItalianGenerator import Falcon7BInstructModel
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
italian_generator = Falcon7BInstructModel()

# Get the collection for the embeddings
collection = embedding_dao.get_or_create_collection("reviews")

counter = 0

# Loop per processare i messaggi
for message in consumer:
    print("-------------MESSAGE VALUE-------------")
    print(message.value["review_body"])

    # Genera l'ID univoco per la recensione
    print("-------------ID VALUE-------------")
    unique_id = generate_id_from_text(message.value["review_body"])
    print(unique_id)
    
    # Generate embedding for the review body
    print("-------------EMBEDDING VALUE-------------")
    embedding = textEmbedder.embed(message.value["review_body"])
    print(embedding)

    # Generate metadata for the review
    print("-------------METADATA VALUE-------------")
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
    counter = counter + 1
    if counter == 5:
        break

while True:        
    # Query the collection
    query_text = input("Enter your query: ")
    company_name = input("Enter company name to filter by (or press Enter to skip): ")

    results = textEmbedder.query_db(query_text, collection, company_name=company_name)

    # Print results
    cleaned_reviews = None
    print("Query results:")
    for result in results['documents']:
        print(f"- {result}")
        # Remove newline characters from each review
        cleaned_reviews = [item.replace('\n', ' ') for item in result]
    
    # Join the cleaned reviews into a single string with enumeration and newline characters
    joined_reviews = "\n".join(cleaned_reviews)
    
    # Construct the prompt with context
    prompt = f"Basato sui seguenti feedback:\n{joined_reviews}\n\nRispondi alla domanda: {query_text}"

    # Generate the response
    response = italian_generator.generate_answer(prompt)
    print("-------------RESPONSE VALUE-------------")
    print(f"Response: {response}")


