from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, FloatType
from embedding.embedder import TextEmbedder
from dao.EmbeddingDao import EmbeddingDao
from codeKafka.utils import generate_id_from_text
import multiprocessing
import logging

# Create a logger
logger = logging.getLogger('MySparkApp')
logger.setLevel(logging.INFO)  # Set the logging level

multiprocessing.set_start_method('fork', force=True)

embedding_dao = EmbeddingDao()
# Get the collection for the embeddings
collection = embedding_dao.get_or_create_collection("reviews")

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkEmbeddings") \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("ERROR")

# Factory function to create an instance of TextEmbedder
def get_text_embedder():
    text_embedder = TextEmbedder()
    text_embedder.load_model()
    return text_embedder

# UDF that uses the TextEmbedder instance
@udf(ArrayType(FloatType()))
def compute_embedding(review_body):
    text_embedder = get_text_embedder()  # Create a new instance for each call
    return text_embedder.embed(review_body)

# Read from Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "host.docker.internal:9093") \
  .option("subscribe", "reviews") \
  .option("startingOffsets", "earliest") \
  .load()

# Convert the Kafka value to string (JSON format)
df = df.selectExpr("CAST(value AS STRING)")

# Parse the JSON data
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType

schema = StructType([
    StructField("review_body", StringType(), True),
    StructField("company_name", StringType(), True),
    StructField("review_title", StringType(), True),
    StructField("review_score", StringType(), True)
])

df_parsed = df.withColumn("data", from_json(col("value"), schema)).select("data.*")

def save_to_chromadb(df, batch_id):
    for row in df.collect():
        logger.info(f"Processing row: {row}")
        metadata = {
            'company_name': row['company_name'],
            'review_title': row['review_title'],
            'review_score': row['review_score'],
            'ins_timestamp': datetime.now().isoformat()
        }
        embedding_dao.save(
            documents=[row['review_body']],
            embeddings=get_text_embedder().embed(row['review_body']),
            collection=collection,
            metadatas=[metadata],
            ids=[generate_id_from_text(row['review_body'])]
        )
        logger.info(f"Saved to ChromaDB: {row}")

# Use `foreachBatch` to save the embeddings to ChromaDB
query = df_parsed.writeStream \
    .foreachBatch(save_to_chromadb) \
    .start()

query.awaitTermination()