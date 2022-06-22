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

splitted = raw_data.withColumn('words', F.explode(F.split('full_text', ' ')))
nohashes = splitted.where(splitted.words.startswith('#') == False)
nolinks = nohashes.where(nohashes.words.startswith('http:') == False)
noslinks = nolinks.where(nolinks.words.startswith('https:') == False)
wtime = noslinks.withColumn('timestamp', F.current_timestamp())
grouped = wtime.withWatermark('timestamp', '5 seconds').groupBy('id', 'timestamp').agg(F.concat_ws(',', F.collect_list(wtime.words)).alias('full_text'))
concatted = grouped.select('id', 'timestamp', F.regexp_replace('full_text', ',', ' ').alias('full_text'))
decoded = concatted.select('id', 'timestamp', unescape_udf('full_text').alias('full_text'))
alphanum = decoded.withColumn('full_text', F.regexp_replace('full_text', '[^A-Za-z0-9 ]+', '').alias('full_text'))
lowerc = alphanum.select('id','timestamp', F.lower('full_text').alias('full_text'))

streamingQuery = lowerc.writeStream \
    .format("csv") \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .option("checkpointLocation", os.environ['HOME'] + '/Projects/twitter-sentiment/checkpoint') \
    .start(os.environ['HOME'] + '/Projects/twitter-sentiment/processed')

streamingQuery.awaitTermination()

spark.stop()
