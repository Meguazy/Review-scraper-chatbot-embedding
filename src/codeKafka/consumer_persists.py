from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaToHDFS") \
    .config("spark.sql.streaming.checkpointLocation", "./spark_checkpoint") \
    .getOrCreate()
    
print("Spark session started")

# Kafka configuration
kafka_bootstrap_servers = "localhost:9093"
kafka_topic = "reviews"

# Read data from Kafka
kafka_stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()
    
print("Reading data from Kafka")

# Extract the value from Kafka (assuming it's in JSON format)
reviews_df = kafka_stream_df.selectExpr("CAST(value AS STRING)")

# Parse JSON data and create a DataFrame with the desired schema
reviews_df = reviews_df.selectExpr(
    "json_extract(value, '$.company_name') AS company_name",
    "json_extract(value, '$.review_title') AS review_title",
    "json_extract(value, '$.review_body') AS review_body",
    "json_extract(value, '$.review_score') AS review_score"
)

# Define HDFS configuration
hdfs_path = "hdfs://namenode:50070/persist_raw"

# Write data to HDFS
query = reviews_df.writeStream \
    .format("parquet") \
    .option("path", hdfs_path) \
    .option("checkpointLocation", "./checkpoint_kafka") \
    .outputMode("append") \
    .start()

# Await termination
query.awaitTermination()
