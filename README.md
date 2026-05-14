# Sobiya_K_DE_Capstone
# Global Earthquake Monitor Pipeline

A fully automated data engineering pipeline that collects live earthquake data daily, enriches it with weather and country information, and visualizes the results in an interactive Streamlit dashboard.

---

## Data Question

**How do earthquake frequency and magnitude vary by region over time?**

---

## Data Sources

| API | Description | Cost |
|---|---|---|
| USGS Earthquake API | Live earthquake data updated every few minutes | Free |
| Open-Meteo API | Weather conditions at each earthquake location | Free |
| REST Countries API | Country and region details | Free |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python |
| Orchestration | Apache Airflow 3.0 |
| Raw Storage | AWS S3 |
| Database | PostgreSQL |
| Transformation | dbt |
| Dashboard | Streamlit |
| Containerization | Docker |
| Code Quality | Ruff |
| Testing | Pytest |

---

## Pipeline Flow
USGS API          → ingest_earthquakes.py  → AWS S3 (raw)  ─┐
Open-Meteo API    → ingest_weather.py      → AWS S3 (raw)  ─┼→ PostgreSQL → dbt staging → dbt marts → Streamlit
REST Countries API → ingest_countries.py  → AWS S3 (raw)  ─┘

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/NSS-Data-Engineering-Oct2025/Sobiya_K_DE_Capstone.git
cd Sobiya_K_DE_Capstone
```

**2. Install dependencies**
```bash
uv add requests boto3 pandas psycopg2-binary python-dotenv dbt-postgres streamlit pytest ruff
```

**3. Set up your environment variables**

Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```

Your `.env` file should contain:
```bash
# PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_NAME=earthquake_db
DB_USER=postgres
DB_PASSWORD=yourpassword

# AWS S3
AWS_PROFILE=your_aws_profile
AWS_REGION=us-west-2
S3_BUCKET_NAME=your_bucket_name
S3_PREFIX=your/folder/path/

# API URLs
USGS_URL=https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson
OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast
REST_COUNTRIES_URL=https://restcountries.com/v3.1/name/

# Email Alerts
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

# Airflow
AIRFLOW__CORE__LOAD_EXAMPLES=false
```

**4. Start Docker**
```bash
docker-compose up --build
```

**5. Log into Airflow**

Go to `http://localhost:8080` and trigger the `earthquake_pipeline` DAG

**6. Run the dashboard**
```bash
uv run streamlit run dashboard.py
```

---

## Running Tests

```bash
uv run pytest earthquake_dbt/tests/ -v
```

---

## Project Structure
Sobiya_K_DE_Capstone/
├── dags/
│   └── earthquake_dag.py        # Airflow DAG
├── ingest/
│   ├── ingest_earthquakes.py    # USGS API ingestion
│   ├── ingest_weather.py        # Open-Meteo API ingestion
│   ├── ingest_countries.py      # REST Countries API ingestion
│   └── load_to_db.py            # Load S3 data to PostgreSQL
├── earthquake_dbt/
│   └── models/
│       ├── staging/             # Clean and rename raw data
│       └── marts/               # Join all 3 datasets
├── dashboard.py                 # Streamlit dashboard
├── docker-compose.yml
├── dockerfile
├── .env.example
└── README.md

---

## Key Findings

- **Americas** had the most earthquakes (98) but the lowest average magnitude (2.72)
- **Europe and Asia** had fewer earthquakes but stronger ones on average (4.5+)
- **Top 5 most powerful earthquakes** were all located in Asia — Japan and Indonesia
- Biggest recorded: **5.7 magnitude near Koya, Japan**