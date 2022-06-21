from concurrent.futures import process
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
#wtime = noslinks.withColumn('timestamp', F.to_timestamp('created_at', 'E M dd HH:mm:ss x yyyy'))
grouped = wtime.groupBy('id', 'timestamp').agg(F.concat_ws(',', F.collect_list(wtime.words)).alias('full_text'))
concatted = grouped.select('id', 'timestamp', F.regexp_replace('full_text', ',', ' ').alias('full_text'))
decoded = concatted.select('id', 'timestamp', unescape_udf('full_text').alias('full_text'))
alphanum = decoded.withColumn('full_text', F.regexp_replace('full_text', '[^A-Za-z0-9 ]+', '').alias('full_text'))
lowerc = alphanum.select('id','timestamp', F.lower('full_text').alias('full_text'))

checkpointDir = os.environ['HOME'] + '/Projects/twitter-sentiment/checkpoint'
streamingQuery = lowerc.writeStream \
    .format("console") \
    .outputMode("complete") \
    .trigger(processingTime='1 minute') \
    .start()
    # .option("checkpointLocation", checkpointDir) \
    # .start(os.environ['HOME'] + '/Projects/twitter-sentiment/processed')

streamingQuery.awaitTermination()

spark.stop()

