from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import LogisticRegression

spark = SparkSession.builder.appName('TrainTwitterSentimentModel').getOrCreate()

df = spark.read.parquet('processed')

(train_set, test_set) = df.randomSplit([0.8, 0.2], seed = 42)

# Converting text to an array of words
tokenizer = Tokenizer(inputCol="full_text", outputCol="words")

# Converting words to numerical format using TF-IDF strategy
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5)

# Converting targets to index format
label_stringIdx = StringIndexer(inputCol = "target", outputCol = "label")

# Training the model
lr = LogisticRegression(maxIter=100)
pipeline = Pipeline(stages=[tokenizer, hashtf, idf, label_stringIdx, lr])
model = pipeline.fit(train_set)
predictions = model.transform(test_set)

predictions.show()
accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(test_set.count())
print('Accuracy: %.2f' % accuracy)

spark.stop()

