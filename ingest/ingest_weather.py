import requests
import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# API URL
OPEN_METEO_URL = os.getenv("OPEN_METEO_URL")

# S3 Config
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")
AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")

def ingest_weather(earthquakes):
    print(f"Fetching weather data at {datetime.now()}")

    weather_data = []

    for quake in earthquakes:
        # Get coordinates from each earthquake
        lon, lat, depth = quake["geometry"]["coordinates"]
        quake_id = quake["id"]

        # Call Open-Meteo API
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        response = requests.get(OPEN_METEO_URL, params=params)

        if response.status_code == 200:
            weather = response.json()
            weather["earthquake_id"] = quake_id
            weather["latitude"] = lat
            weather["longitude"] = lon
            weather_data.append(weather)
            print(f"Got weather for earthquake {quake_id}")

        else:
            print(f"Failed to get weather for {quake_id}: {response.status_code}")

    # Save to S3
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION
    )
    s3 = session.client("s3")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{S3_PREFIX}weather/weather_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=json.dumps(weather_data, indent=2),
        ContentType="application/json"
    )

    print(f"Weather data saved to s3://{S3_BUCKET}/{filename}")
    return weather_data

if __name__ == "__main__":
    url = os.getenv("USGS_URL")
    response = requests.get(url)
    earthquakes = response.json()["features"]
    print(f"Loaded {len(earthquakes)} earthquakes for weather enrichment")
    ingest_weather(earthquakes)