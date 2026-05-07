import requests
import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# S3 Config
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")
AWS_REGION = os.getenv("AWS_REGION")
AWS_PROFILE = os.getenv("AWS_PROFILE")
REST_COUNTRIES_URL = os.getenv("REST_COUNTRIES_URL")

# List of countries to fetch
COUNTRIES = [
    "united states", "japan", "indonesia", "chile",
    "mexico", "turkey", "italy", "greece", "iran", "china"
]

def ingest_countries():
    print(f"Fetching country data at {datetime.now()}")

    countries_data = []

    for country in COUNTRIES:
        response = requests.get(f"{REST_COUNTRIES_URL}{country}")

        if response.status_code == 200:
            data = response.json()
            # Take first result only
            country_info = {
                "name": data[0]["name"]["common"],
                "region": data[0]["region"],
                "subregion": data[0].get("subregion", ""),
                "continents": data[0]["continents"],
                "population": data[0]["population"],
                "capital": data[0].get("capital", [""])[0],
                "latlng": data[0]["latlng"]
            }
            countries_data.append(country_info)
            print(f"Got data for {country_info['name']}")

        else:
            print(f"Failed to get data for {country}: {response.status_code}")

    # Save to S3
    session = boto3.Session(
    profile_name=AWS_PROFILE,
    region_name=AWS_REGION
    )
    s3 = session.client("s3")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{S3_PREFIX}countries/countries_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=json.dumps(countries_data, indent=2),
        ContentType="application/json"
    )

    print(f"Country data saved to s3://{S3_BUCKET}/{filename}")
    return countries_data

if __name__ == "__main__":
    ingest_countries()