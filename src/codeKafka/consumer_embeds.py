from kafka import KafkaConsumer
from embedding.embedder import TextEmbedder

import json

consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers=['localhost:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

textEmbedder = TextEmbedder()

# note that this for loop will block forever to wait for the next message
for message in consumer:
    print("-------------MESSAGE VALUE-------------")
    print(message.value["review_body"])

    tokens = textEmbedder.tokenize_sentence(message.value["review_body"])
    for token in tokens:
        print("-------------TOKENIZATION VALUE-------------")
        print(token)

        embedding = textEmbedder.embed(token)

        print("-------------EMBEDDING VALUE-------------")
        print(embedding)