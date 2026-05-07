import requests
import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# API URL
USGS_URL = os.getenv("USGS_URL")

# S3 Config
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")
AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")

def ingest_earthquakes():
    print(f"Fetching earthquake data at {datetime.now()}")

    response = requests.get(USGS_URL)

    if response.status_code == 200:
        data = response.json()
        earthquakes = data["features"]
        print(f"Fetched {len(earthquakes)} earthquakes")

        session = boto3.Session(
            profile_name=AWS_PROFILE,
            region_name=AWS_REGION
        )
        s3 = session.client("s3")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{S3_PREFIX}earthquakes/earthquakes_{timestamp}.json"

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=json.dumps(earthquakes, indent=2),
            ContentType="application/json"
        )

        print(f"Raw data saved to s3://{S3_BUCKET}/{filename}")
        return earthquakes

    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    ingest_earthquakes()