from elasticsearch import Elasticsearch


def create_index(index_name):
    es = Elasticsearch(hosts=["http://localhost:9200"])

    # Definisci il mapping
    mapping = {
        "mappings": {
            "properties": {
                "company_name": {"type": "keyword"},
                "review_title": {"type": "text"},
                "review_body": {"type": "text"},
                "review_score": {"type": "float"},
                "sentiment": {"type": "keyword"}
            }
        }
    }

    # Crea l'indice se non esiste già
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"Indice '{index_name}' creato con successo.")
    else:
        print(f"L'indice '{index_name}' esiste già.")


if __name__ == "__main__":
    index_name = input("Inserisci il nome del nuovo indice: ")
    create_index(index_name)
