import requests

def test_usgs_api_returns_data():
    """Test USGS API returns earthquake data"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "features" in data
    assert len(data["features"]) > 0

def test_open_meteo_api_returns_data():
    """Test Open-Meteo API returns weather data"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": 38.71, "longitude": -117.05, "current_weather": True}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    assert "current_weather" in data

def test_rest_countries_api_returns_data():
    """Test REST Countries API returns country data"""
    url = "https://restcountries.com/v3.1/name/japan"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_earthquake_has_required_fields():
    """Test each earthquake has magnitude, place and coordinates"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    earthquakes = response.json()["features"]
    for quake in earthquakes[:5]:
        assert "mag" in quake["properties"]
        assert "place" in quake["properties"]
        assert len(quake["geometry"]["coordinates"]) == 3