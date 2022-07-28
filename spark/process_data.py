import os
import html
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sentiment = SentimentIntensityAnalyzer()

spark = SparkSession.builder \
    .appName('TwitterSentiment') \
    .getOrCreate()

schema = "id LONG, created_at STRING, full_text STRING"
raw_data = spark.read \
    .schema(schema) \
    .json('/shared/tweets_*.json')

# UDF aimed to remove html escaped characters
def unescape_string(escaped):
    return html.unescape(escaped)
unescape_udf = F.udf(unescape_string)

# UDF aimed to perform sentiment analysis
def label_data(text):
    sentiment_dict = sentiment.polarity_scores(text)

    if sentiment_dict['pos'] >= 0.05:
        return 1
    elif sentiment_dict['neg'] >= 0.05:
        return -1
    else:
        return 0
label_data_udf = F.udf(label_data, returnType='INTEGER')

duplicates = raw_data.where(raw_data.full_text.startswith('RT') == False)
splitted = duplicates.withColumn('words', F.explode(F.split('full_text', ' '))) \
    .withColumn('timestamp', F.to_timestamp(raw_data.created_at.substr(5,28), 'MMM dd HH:mm:ss xxxx yyyy'))
filtered = splitted.where(splitted.words.startswith('#') == False) \
    .where(splitted.words.startswith('@') == False) \
    .where(splitted.words.startswith('http:') == False) \
    .where(splitted.words.startswith('https:') == False)
grouped = filtered.withWatermark('timestamp', '50 seconds') \
    .groupBy('id', 'timestamp') \
    .agg(F.concat_ws(' ', F.collect_list(filtered.words)).alias('full_text'))
cleaned = grouped.select('id', 'full_text') \
    .withColumn('full_text', unescape_udf('full_text')) \
    .withColumn('full_text', F.regexp_replace('full_text', '[^A-Za-z0-9 ]+', '')) \
    .withColumn('full_text', F.lower('full_text')) \
    .withColumn('target', label_data_udf('full_text'))

cleaned.show()

spark.stop()
