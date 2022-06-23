from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable

with DAG(
    'twitter_sentiment_analysis',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
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
    },
    description='Twitter sentiment analysis DAG',
    schedule_interval="* * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['tweets'],
) as dag:

    arg = Variable.get("twitter_sentiment_analysis_download_tweets_arg")
    t1 = BashOperator(
        task_id='download_tweets',
        depends_on_past=False,
        bash_command='python3 ~/Projects/twitter-sentiment/download_data.py ' + arg
    )

    t1
