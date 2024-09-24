zip -r dependencies.zip embedding/ dao/ scraper/ codeKafka/

spark-submit \
  --master local[*] \
  --deploy-mode client \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 \
  --py-files dependencies.zip \
 codeKafka/spark_embeds.py