FROM python:3.8-slim-buster

# Airflow setup                      
ENV AIRFLOW_HOME=/app/airflow
RUN mkdir -p $AIRFLOW_HOME/dags
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install vim iputils-ping nmap

EXPOSE 8080

WORKDIR $AIRFLOW_HOME

COPY entrypoint.sh .
COPY airflow.cfg_local .
COPY dags/* $AIRFLOW_HOME/dags

ENTRYPOINT ["sh", "entrypoint.sh"]
