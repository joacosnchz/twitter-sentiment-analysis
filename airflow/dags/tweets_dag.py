import os
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'depends_on_past': False,
    'email': ['test@test.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

@dag(
    default_args=default_args,
    schedule_interval='* * * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['tweets'],
)
def twitter_sentiment_analysis():

    t1 = DockerOperator(
        task_id='search_dw', 
        image='twitter-sentiment_scraping:latest', 
        environment={"URLS": "https://www.dw.com/en", "TO_FILE_FOLDER": "/shared"},
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

tweets = twitter_sentiment_analysis()
