import time
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import datetime
from airflow.configuration import conf

default_args = {
    'owner': 'abc',
    'team': 'ABC Exmple',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['abhishek.create@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
}

# {"table_name":"example_abc","input_file":"s3://developement-purpose/user/abhishek_choudhary/samples_output/username-password-partition/part=2019,NA"}

with DAG(
        'Pod_Example',
        default_args=default_args,
        description='Test ABC',
        schedule_interval=None,
        concurrency=10,
        tags=['abc', 'test','example'],
) as dag:
    
    start = DummyOperator(task_id='start', dag=dag, trigger_rule='all_success')
    
    test = KubernetesPodOperator(
        namespace='default',
        image="nginx:1.14.2",
        image_pull_policy="IfNotPresent",
        name="nginx_run",
        task_id="nginx_run",
        dag=dag,
        is_delete_operator_pod=False,
        in_cluster=True,
        startup_timeout_seconds=600,
        get_logs=True
    )


    pytest = KubernetesPodOperator(
        namespace='default',
        image="python-docker:test",
        image_pull_policy="IfNotPresent",
        name="Pytest_Abc",
        task_id="Python_test",
        cmds=["/bin/sh", "-c",
              f"python -u test.py"],
        dag=dag,
        is_delete_operator_pod=False,
        in_cluster=True,
        startup_timeout_seconds=600,
        get_logs=True
    )

    end = DummyOperator(task_id='end', dag=dag, trigger_rule='all_success')

    start >> test 
    start >> pytest
    pytest >> end

