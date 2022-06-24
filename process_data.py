import os
import html
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName('TwitterSentiment').getOrCreate()

schema = "id LONG, full_text STRING"
raw_data = spark.readStream \
    .schema(schema) \
    .json('data/tweets-*.json')

# UDF aimed to remove html escaped characters
def unescape_string(escaped):
    return html.unescape(escaped)
unescape_udf = F.udf(unescape_string)

duplicates = raw_data.where(raw_data.full_text.startswith('RT') == False) \
    .dropDuplicates(['id'])
splitted = duplicates.withColumn('words', F.explode(F.split('full_text', ' '))) \
    .withColumn('timestamp', F.current_timestamp())
filtered = splitted.where(splitted.words.startswith('#') == False) \
    .where(splitted.words.startswith('@') == False) \
    .where(splitted.words.startswith('http:') == False) \
    .where(splitted.words.startswith('https:') == False)
grouped = filtered.withWatermark('timestamp', '50 seconds') \
    .groupBy('id', 'timestamp') \
    .agg(F.concat_ws(',', F.collect_list(filtered.words)).alias('full_text')) \
    .select('id', 'timestamp', F.regexp_replace('full_text', ',', ' ').alias('full_text'))
cleaned = grouped.withColumn('full_text', unescape_udf('full_text')) \
    .withColumn('full_text', F.regexp_replace('full_text', '[^A-Za-z0-9 ]+', '')) \
    .withColumn('full_text', F.lower('full_text'))

streamingQuery = cleaned.writeStream \
    .format("csv") \
    .outputMode("append") \
    .trigger(processingTime='55 seconds') \
    .option("checkpointLocation", os.environ['HOME'] + '/Projects/twitter-sentiment/checkpoint') \
    .start(os.environ['HOME'] + '/Projects/twitter-sentiment/processed') \
    .awaitTermination()

spark.stop()
