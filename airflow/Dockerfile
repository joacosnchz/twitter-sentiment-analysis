FROM python:3.8-slim-buster

# Airflow setup                      
ENV AIRFLOW_HOME=/app/airflow
RUN mkdir -p $AIRFLOW_HOME/dags
COPY dags/* $AIRFLOW_HOME/dags
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install vim

EXPOSE 8080

WORKDIR $AIRFLOW_HOME

COPY entrypoint.sh .
COPY airflow.cfg_local .

ENTRYPOINT ["sh", "entrypoint.sh"]
