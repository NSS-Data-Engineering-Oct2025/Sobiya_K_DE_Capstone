import pendulum
from airflow.decorators import dag, task
from airflow.utils.email import send_email


def on_failure(context):
    send_email(
        to=["ksobiya09@gmail.com"],
        subject=f"{context['dag'].dag_id} failed!",
        html_content=f"Task {context['task_instance'].task_id} failed!",
    )


@task
def ingest_earthquakes():
    import sys
    sys.path.insert(0, "/opt/airflow/workspace/ingest")
    from ingest_earthquakes import ingest_earthquakes
    return ingest_earthquakes()


@task
def ingest_weather(earthquakes):
    import sys
    sys.path.insert(0, "/opt/airflow/workspace/ingest")
    from ingest_weather import ingest_weather
    return ingest_weather(earthquakes)


@task
def ingest_countries():
    import sys
    sys.path.insert(0, "/opt/airflow/workspace/ingest")
    from ingest_countries import ingest_countries
    ingest_countries()


@task
def load_to_db():
    import sys
    sys.path.insert(0, "/opt/airflow/workspace/ingest")
    from load_to_db import load_to_db
    load_to_db()


@task
def dbt_run():
    import subprocess
    subprocess.run(
        ["dbt", "run", "--profiles-dir", "/opt/airflow/workspace/earthquake_dbt"],
        cwd="/opt/airflow/workspace/earthquake_dbt",
        check=True
    )


@dag(
    dag_id="earthquake_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["earthquake", "capstone"],
    default_args={"on_failure_callback": on_failure},
)
def earthquake_pipeline():
    earthquakes = ingest_earthquakes()
    weather = ingest_weather(earthquakes)
    countries = ingest_countries()
    load = load_to_db()
    run_dbt = dbt_run()

    earthquakes >> weather >> countries >> load >> run_dbt


earthquake_pipeline = earthquake_pipeline()