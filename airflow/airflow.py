from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'your_name',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'hadoop_streaming_and_python_script',
    default_args=default_args,
    description='Run Hadoop Streaming and Python script',
    schedule_interval=None,  # Set your desired schedule interval
    catchup=False,
)

# Task to run the Hadoop Streaming command
run_hadoop_streaming = BashOperator(
    task_id='run_hadoop_streaming',
    bash_command="mapred streaming -files /usr/local/hadoop/data/my_mapper.py,/usr/local/hadoop/data/my_reducer.py -mapper my_mapper.py -reducer my_reducer.py -input /raw/2023-10-20/22-14-mastodon.json -output /results/result17",
    dag=dag,
)

# Task to run the Python script
run_python_script = BashOperator(
    task_id='run_python_script',
    bash_command="python3 /usr/local/hadoop/data/my_mastodon.py",
    dag=dag,
)

# Define the task dependencies
run_hadoop_streaming >> run_python_script

if __name__ == "__main__":
    dag.cli()
