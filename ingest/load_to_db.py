import boto3
import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# S3 Config
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")
AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")

# DB Config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_to_db():
    # Connect to database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Connect to S3
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION
    )
    s3 = session.client("s3")

    # Helper to get latest file from S3 folder
    def get_latest_file(folder):
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{S3_PREFIX}{folder}/")
        files = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
        key = files[0]["Key"]
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return json.loads(obj["Body"].read())

    # Load earthquakes
    print("Loading earthquakes...")
    earthquakes = get_latest_file("earthquakes")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_earthquakes (
            id VARCHAR PRIMARY KEY,
            magnitude FLOAT,
            place VARCHAR,
            earthquake_time BIGINT,
            tsunami INT,
            significance INT,
            latitude FLOAT,
            longitude FLOAT,
            depth FLOAT
        )
    """)
    for quake in earthquakes:
        props = quake["properties"]
        coords = quake["geometry"]["coordinates"]
        cursor.execute("""
            INSERT INTO raw_earthquakes
            (id, magnitude, place, earthquake_time, tsunami, significance, latitude, longitude, depth)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            quake["id"],
            props.get("mag"),
            props.get("place"),
            props.get("time"),
            props.get("tsunami"),
            props.get("sig"),
            coords[1],
            coords[0],
            coords[2]
        ))
    print(f"Loaded {len(earthquakes)} earthquakes")

    # Load countries
    print("Loading countries...")
    countries = get_latest_file("countries")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_countries (
            name VARCHAR PRIMARY KEY,
            region VARCHAR,
            subregion VARCHAR,
            continents VARCHAR,
            population BIGINT,
            capital VARCHAR,
            latitude FLOAT,
            longitude FLOAT
        )
    """)
    for country in countries:
        cursor.execute("""
            INSERT INTO raw_countries
            (name, region, subregion, continents, population, capital, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (
            country.get("name"),
            country.get("region"),
            country.get("subregion"),
            str(country.get("continents")),
            country.get("population"),
            country.get("capital"),
            country.get("latlng", [None, None])[0],
            country.get("latlng", [None, None])[1]
        ))
    print(f"Loaded {len(countries)} countries")

    # Load weather
    print("Loading weather...")
    weather_data = get_latest_file("weather")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            earthquake_id VARCHAR,
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT
        )
    """)
    for weather in weather_data:
        cw = weather.get("current_weather", {})
        cursor.execute("""
            INSERT INTO raw_weather
            (earthquake_id, latitude, longitude, temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            weather.get("earthquake_id"),
            weather.get("latitude"),
            weather.get("longitude"),
            cw.get("temperature"),
            cw.get("windspeed"),
            cw.get("winddirection"),
            cw.get("weathercode")
        ))
    print(f"Loaded {len(weather_data)} weather records")

    # Save and close
    conn.commit()
    cursor.close()
    conn.close()
    print("All done!")

if __name__ == "__main__":
    load_to_db()