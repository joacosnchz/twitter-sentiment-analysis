FROM python:3.8-slim-buster

RUN apt-get update && \
  apt-get install -y curl vim openjdk-11-jre-headless

WORKDIR /app

RUN curl -o spark-3.3.0-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz && \
  tar -xzf spark-3.3.0-bin-hadoop3.tgz && \
  mv spark-3.3.0-bin-hadoop3 spark && \
  rm spark-3.3.0-bin-hadoop3.tgz && \
  curl -o spark/jars/spark-avro_2.12-3.2.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.2.1/spark-avro_2.12-3.2.1.jar

ENV SPARK_HOME /app/spark
RUN export SPARK_HOME
ENV PATH "$PATH:$SPARK_HOME/bin"

ENV LOCAL_EXES /app/.local/bin
RUN export LOCAL_EXES
ENV PATH "$PATH:$LOCAL_EXES"

#install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY process_data.py .

ENTRYPOINT ["spark-submit", "--packages", "org.mongodb.spark:mongo-spark-connector:10.0.2", "process_data.py"]
