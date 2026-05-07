# Global Earthquake Monitor

A data pipeline that collects live earthquake data daily, enriches it with weather and country information, and displays the results in an interactive dashboard.

## Data Question
How do earthquake frequency and magnitude vary by region over time?

## Data Sources
- USGS Earthquake API - live earthquake data, updates every few minutes
- Open-Meteo API - weather conditions at each earthquake location
- REST Countries API - country and region details

## Tech Stack
- Python - data ingestion
- Apache Airflow - pipeline scheduling and orchestration
- AWS S3 - raw data storage
- PostgreSQL - database
- dbt - data transformation
- Streamlit - dashboard
- Docker - containerization

## Pipeline Flow
USGS API → ingest_earthquakes.py → S3 (raw)
Open-Meteo API → ingest_weather.py → S3 (raw)
REST Countries API → ingest_countries.py → S3 (raw)
load_to_db.py → PostgreSQL
dbt → staging models → marts models
Streamlit → dashboard

## How to Run Locally

1. Clone the repo
git clone [repo url](https://github.com/NSS-Data-Engineering-Oct2025/Sobiya_K_DE_Capstone.git)

2. Install dependencies
uv add requests boto3 pandas psycopg2-binary python-dotenv dbt-postgres streamlit

3. Set up your .env file with your credentials

4. Start Docker
docker-compose up --build

5. Log into Airflow at http://localhost:8080 and trigger the earthquake_pipeline DAG

6. Run the dashboard
uv run streamlit run dashboard.py

## Project Structure
dags/               - Airflow DAG
ingest/             - Ingestion and loading scripts
earthquake_dbt/     - dbt models
  models/
    staging/        - cleaning and renaming
    marts/          - final joined table
dashboard.py        - Streamlit dashboard
docker-compose.yml
dockerfile
.env