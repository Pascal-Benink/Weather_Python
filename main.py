import datetime
import json
import os
from dotenv import load_dotenv
import requests
from requests import get

from sql_client import SQLClient

load_dotenv()
sql_client = SQLClient()

def get_weather_from_ip():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    max_bike_distance = config_data["max_bike_distance"]
    max_bike_temp = config_data["max_bike_temp"]
    min_bike_temp = config_data["min_bike_temp"]

    ip = get('https://api.ipify.org').content.decode('utf8')

    api_key = os.getenv("API_KEY")
    api_url_base = os.getenv("API_URL")

    url = f"{api_url_base}/locations/v1/cities/ipaddress?apikey={api_key}&q={ip}"

    response = requests.get(url)
    location_data_unformatted = response.json()
    location_data = [location_data_unformatted]

    location_key = location_data[0]['Key']
    conditions_url = f"{api_url_base}/currentconditions/v1/{location_key}"
    conditions_params = {
        'apikey': api_key
    }

    conditionsResponse = requests.get(conditions_url, params=conditions_params)
    conditions_data = conditionsResponse.json()

    create_tables()

    current_weather = conditions_data[0]['WeatherText']
    current_weather_ic = conditions_data[0]['WeatherIcon']
    current_temp = conditions_data[0]['Temperature']['Metric']['Value']
    lat = location_data[0]['GeoPosition']['Latitude']
    lon = location_data[0]['GeoPosition']['Longitude']
    current_float_temp = float(current_temp)

    max_bike_temp = float(max_bike_temp)
    min_bike_temp = float(min_bike_temp)

    distance = config_data["bike_distance"]

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    temp = chk_temp(current_float_temp, max_bike_temp, min_bike_temp)
    bike_distance = chk_bike_distance(distance, max_bike_distance)

    response_data = {
        "Temperature": current_temp,
        "Weather": current_weather,
        "icon": current_weather_ic,
        "bikeable": chk_bike(temp, bike_distance),
        "Lat": lat,
        "Lon": lon,
        "Saved_at": formatted_time,
    }
    insertable = {
        "Temperature": current_temp,
        "Weather": current_weather,
        "icon": current_weather_ic,
        "Latitude": lat,
        "Longitude": lon,
        "Saved_at": formatted_time,
    }
    insertdata(insertable)

    return response_data

def create_tables():
    weather_table = "Weather_table"

    # Check if Weather table exists
    if not sql_client.check_table_exists(weather_table):
        # Create Weather table if it doesn't exist
        create_weather_table_query = """
            CREATE TABLE Weather_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Weather VARCHAR(255) NOT NULL,
                Icon INT NOT NULL,
                Temperature FLOAT NOT NULL,
                Latitude FLOAT NOT NULL,
                Longitude FLOAT NOT NULL,
                Saved_at VARCHAR(255) NOT NULL
            );"""
        sql_client.query_fix(create_weather_table_query)

def insertdata(insertable):

    Weather = insertable.get("Weather")
    Icon = insertable.get("icon")
    Temperature = insertable.get("Temperature")
    Latitude = insertable.get("Latitude")
    Longitude = insertable.get("Longitude")
    Saved_at = insertable.get("Saved_at")

    keys = ["Weather", "icon", "Temperature", "Latitude", "Longitude", "Saved_at"]
    keys = tuple(keys)
    values = [Weather, Icon, Temperature, Latitude, Longitude, Saved_at]
    values = tuple(values)
    table_name = "Weather_table"
    sql_client.insert(keys, values, table_name)

def chk_temp(current_temp, maxtemp, mintemp):
    if current_temp >= mintemp:
        mintemp_chk = True
    else:
        mintemp_chk = False

    if current_temp <= maxtemp:
        maxtemp_chk = True
    else:
        maxtemp_chk = False

    if maxtemp_chk == True and mintemp_chk == True:
        return True

def chk_bike_distance(distance, max_bike_distance):
    if distance <= max_bike_distance:
        return True
    else:
        return False

def chk_bike(temp, distance):
    if temp and distance:
        return True

if __name__ == '__main__':
    weather = get_weather_from_ip()
    print(weather)