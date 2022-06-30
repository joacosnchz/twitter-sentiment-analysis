import os
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from download_data import download
from dw_scraper import search

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

    @task()
    def download_tweets(query):
        download(query, os.environ['HOME'] + '/Projects/twitter-sentiment')

    @task()
    def search_dw():
        return search()

    t1 = search_dw()
    t2 = download_tweets(t1)

tweets = twitter_sentiment_analysis()
