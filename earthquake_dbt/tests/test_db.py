import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(
        host="localhost",
        port="5440",
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def test_raw_earthquakes_table_exists():
    """Test raw_earthquakes table exists"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'raw_earthquakes')")
    exists = cur.fetchone()[0]
    conn.close()
    assert exists

def test_raw_weather_table_exists():
    """Test raw_weather table exists"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'raw_weather')")
    exists = cur.fetchone()[0]
    conn.close()
    assert exists

def test_raw_countries_table_exists():
    """Test raw_countries table exists"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'raw_countries')")
    exists = cur.fetchone()[0]
    conn.close()
    assert exists

def test_earthquakes_have_data():
    """Test earthquakes table has records"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM raw_earthquakes")
    count = cur.fetchone()[0]
    conn.close()
    assert count > 0