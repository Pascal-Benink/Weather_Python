import datetime
import json
import os
from dotenv import load_dotenv
import requests
from requests import get
load_dotenv()

def get_weather_from_ip():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    max_bike_distance = config_data["max_bike_distance"]
    max_bike_temp = config_data["max_bike_temp"]
    min_bike_temp = config_data["min_bike_temp"]

    ip = get('https://api.ipify.org').content.decode('utf8')

    location_key = ""
    api_key = os.getenv("API_KEY")
    api_url_base = os.getenv("API_URL")

    url = f"{api_url_base}/locations/v1/cities/ipaddress"

    params = {
        'api_key': api_key,
        'q': ip
    }

    response = requests.get(url, params=params)
    location_data = response.json()

    location_key = location_data[0]['Key']
    conditions_url = f"{api_url_base}/currentconditions/v1/{location_key}"
    conditions_params = {
        'apikey': api_key
    }
    print(location_data)
    conditionsResponse = requests.get(conditions_url, params=conditions_params)
    response_text = conditionsResponse.text
    print(conditionsResponse)
    conditions_data = conditionsResponse.json()

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
        "Temprature": current_temp,
        "Weather": current_weather,
        "icon": current_weather_ic,
        "bikeable": chk_bike(temp, bike_distance),
        "Lat": lat,
        "Lon": lon,
        "Saved_at": formatted_time,
    }

    return response_data

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