from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon')

spark = SparkSession.builder.appName('TrainTwitterSentimentModel').getOrCreate()

schema = 'id LONG, timestamp TIMESTAMP, full_text STRING'
df = spark.read \
    .schema(schema) \
    .option('header', 'false') \
    .csv('processed')

sid_obj = SentimentIntensityAnalyzer()
def label_data(text):
    sentiment_dict = sid_obj.polarity_scores(text)

    if sentiment_dict['pos'] >= 0.05:
        return 1
    elif sentiment_dict['neg'] >= 0.05:
        return -1
    else:
        return 0

label_data_udf = F.udf(label_data, returnType='INTEGER')
df.select('full_text', label_data_udf('full_text').alias('label')).show()
