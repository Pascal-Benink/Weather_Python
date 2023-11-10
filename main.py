import datetime
import json
import os
from dotenv import load_dotenv
import requests
from requests import get
from flask import Flask

from sql_client import SQLClient

load_dotenv()
sql_client = SQLClient()
api_key = os.getenv("API_KEY")
api_url_base = os.getenv("API_URL")

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_weather_from_ip_main():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours=1)

    formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_one_hour_ago = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    max_bike_distance = config_data["max_bike_distance"]
    max_bike_temp = config_data["max_bike_temp"]
    min_bike_temp = config_data["min_bike_temp"]

    time_data_db = get_time_from_db()

    if not time_data_db >= formatted_one_hour_ago:
        response_data = api_response(formatted_current_time, max_bike_distance, max_bike_temp, min_bike_temp,
                                     config_data)
    else:
        response_data = db_response(max_bike_distance, max_bike_temp, min_bike_temp, config_data)

    return response_data


def get_ip():
    try:
        ip = get('https://api.ipify.org').content.decode('utf8')
    except requests.exceptions.HTTPError as ce:
        print(f"Connection Problem: {ce}")
    return ip


def get_location_from_ip_api(ip, api_key, api_url_base):
    url = f"{api_url_base}/locations/v1/cities/ipaddress?apikey={api_key}&q={ip}"

    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as ce:
        print(f"Connection Problem: {ce}")
    location_data_unformatted = response.json()
    return [location_data_unformatted]


def get_weather_from_location_api(location_key, api_key, api_url_base):
    conditions_url = f"{api_url_base}/currentconditions/v1/{location_key}"
    conditions_params = {
        'apikey': api_key
    }

    try:
        conditionsResponse = requests.get(conditions_url, params=conditions_params)
    except requests.exceptions.HTTPError as ce:
        print(f"Connection Problem: {ce}")

    return conditionsResponse.json()


def get_time_from_db():
    if sql_client.check_table_exists("weather_table"):
        try:
            time = sql_client.fetch_all(
                "SELECT saved_at FROM weather_table WHERE `id` = (SELECT MAX(`id`) FROM weather_table);"
            )
            time = time[0]
        except Exception as e:
            print(f"Error: {e}")
        return time['saved_at']
    else:
        return "1970-01-01 00:00:00"


def get_weather_from_db():
    if check_tabel_existence:
        try:
            data = sql_client.fetch_all(
                "SELECT * FROM weather_table WHERE `id` = (SELECT MAX(`id`) FROM weather_table);"
            )
        except Exception as e:
            print(f"Error: {e}")
        return data


def api_response(formatted_current_time, max_bike_distance, max_bike_temp, min_bike_temp, config_data):
    ip = get_ip

    location_data = get_location_from_ip_api(ip, api_key, api_url_base)

    location_key = location_data[0]['Key']

    conditions_data = get_weather_from_location_api(location_key, api_key, api_url_base)

    create_tables()

    current_weather = conditions_data[0]['WeatherText']
    current_weather_icon = conditions_data[0]['WeatherIcon']
    current_temprature = conditions_data[0]['Temperature']['Metric']['Value']
    lat = location_data[0]['GeoPosition']['Latitude']
    lon = location_data[0]['GeoPosition']['Longitude']
    current_float_temp = float(current_temprature)

    max_bike_temp = float(max_bike_temp)
    min_bike_temp = float(min_bike_temp)

    distance = config_data["bike_distance"]

    temp = check_temprature(current_float_temp, max_bike_temp, min_bike_temp)
    bike_distance = check_bike_distance(distance, max_bike_distance)

    response_data = {
        "temperature": current_temprature,
        "weather": current_weather,
        "icon": current_weather_icon,
        "bikeable": check_bike(temp, bike_distance),
        "latitude": lat,
        "longitude": lon,
        "saved_at": formatted_current_time,
    }
    insertable = {
        "temperature": current_temprature,
        "weather": current_weather,
        "icon": current_weather_icon,
        "latitude": lat,
        "longitude": lon,
        "saved_at": formatted_current_time,
    }
    insertdata(insertable)

    return response_data


def db_response(max_bike_distance, max_bike_temp, min_bike_temp, config_data):
    conditions_data = get_weather_from_db()

    current_weather = conditions_data[0]['weather']
    current_weather_icon = conditions_data[0]['icon']
    current_temprature = conditions_data[0]['temperature']
    lat = conditions_data[0]['latitude']
    lon = conditions_data[0]['longitude']
    saved_at = conditions_data[0]['saved_at']
    current_float_temp = float(current_temprature)

    max_bike_temp = float(max_bike_temp)
    min_bike_temp = float(min_bike_temp)

    distance = config_data["bike_distance"]

    temp = check_temprature(current_float_temp, max_bike_temp, min_bike_temp)
    bike_distance = check_bike_distance(distance, max_bike_distance)

    response_data = {
        "temperature": current_temprature,
        "weather": current_weather,
        "icon": current_weather_icon,
        "bikeable": check_bike(temp, bike_distance),
        "latitude": lat,
        "longitude": lon,
        "saved_at": saved_at,
    }
    return response_data


def check_tabel_existence():
    sql_client.check_table_exists("weather_table")


def create_tables():
    weather_table = "weather_table"

    # Check if weather table exists
    if not sql_client.check_table_exists(weather_table):
        # Create weather table if it doesn't exist
        create_weather_table_query = """
            CREATE TABLE weather_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weather VARCHAR(255) NOT NULL,
                icon INT NOT NULL,
                temperature FLOAT NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                saved_at VARCHAR(255) NOT NULL
            );"""
        sql_client.query_fix(create_weather_table_query)


def insertdata(insertable):
    weather = insertable.get("weather")
    Icon = insertable.get("icon")
    temperature = insertable.get("temperature")
    latitude = insertable.get("latitude")
    longitude = insertable.get("longitude")
    saved_at = insertable.get("saved_at")

    keys = ["weather", "icon", "temperature", "latitude", "longitude", "saved_at"]
    keys = tuple(keys)
    values = [weather, Icon, temperature, latitude, longitude, saved_at]
    values = tuple(values)
    table_name = "weather_table"
    sql_client.insert(keys, values, table_name)


def check_temprature(current_temprature, max_temprature, min_temprature):
    if current_temprature >= min_temprature:
        min_temprature_check = True
    else:
        min_temprature_check = False

    if current_temprature <= max_temprature:
        max_temprature_check = True
    else:
        max_temprature_check = False

    return max_temprature_check and min_temprature_check


def check_bike_distance(distance, max_bike_distance):
    if distance <= max_bike_distance:
        return True
    else:
        return False


def check_bike(temp, distance):
    if temp and distance:
        return True
    else:
        return False



if __name__ == '__main__':
    app.run(debug=True)
