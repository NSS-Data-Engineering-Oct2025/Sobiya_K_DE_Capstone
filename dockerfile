FROM apache/airflow:3.0.0-python3.12

RUN pip install --no-cache-dir \
    requests>=2.32.0 \
    pandas>=2.2.0 \
    psycopg2-binary>=2.9.0 \
    python-dotenv>=1.0.0 \
    streamlit>=1.35.0 \
    boto3>=1.34.0 \
    dbt-postgres>=1.8.0 \
    loguru