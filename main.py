import datetime
import json
import os
from dotenv import load_dotenv
import requests
from requests import get

load_dotenv()

print("starting Tracefy© weather checker")

# get configurable preference data from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

max_bike_distance = config_data["max_bike_distance"]
max_bike_temp = config_data["max_bike_temp"]
min_bike_temp = config_data["min_bike_temp"]

ip = get('https://api.ipify.org').content.decode('utf8')

location_key = ""
api_key = os.getenv("API_KEY")

url = f"http://dataservice.accuweather.com/locations/v1/cities/ipaddress?q={ip}&apikey={api_key}"

response = requests.get(url)



location_data = response.json()

if location_data['Code'] == 'ServiceUnavailable':
    print('Service currently unavailable, falling back to mock data')
    data_avalability = False

if data_avalability == True:
    location_key = location_data['Key']
    conditionsUrl = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    conditionsResponse = requests.get(conditionsUrl)
    conditions_data = conditionsResponse.json()
    lat = location_data['GeoPosition']['Latitude']
    lon = location_data['GeoPosition']['Longitude']
else:
    conditions_data = [{
    "LocalObservationDateTime": "2023-11-06T10:32:00+01:00",
    "EpochTime": 1699263120,
    "WeatherText": "Mostly cloudy",
    "WeatherIcon": 6,
    "HasPrecipitation": False,
    "PrecipitationType": None,
    "IsDayTime": True,
    "Temperature": {
      "Metric": {
        "Value": 10,
        "Unit": "C",
        "UnitType": 17
      },
      "Imperial": {
        "Value": 50,
        "Unit": "F",
        "UnitType": 18
      }
    },
    "MobileLink": "http://www.accuweather.com/en/nl/de-eenhoorn/3510033/current-weather/3510033?lang=en-us",
    "Link": "http://www.accuweather.com/en/nl/de-eenhoorn/3510033/current-weather/3510033?lang=en-us"
  }]
    lat = '52.35'
    lon = '4.922'


# print(location_data)
#
# print(conditions_data)

current_weather = conditions_data[0]['WeatherText']
current_weather_ic = conditions_data[0]['WeatherIcon']
current_temp = conditions_data[0]['Temperature']['Metric']['Value']
current_float_temp = float(current_temp)


max_bike_temp = float(max_bike_temp)
min_bike_temp = float(min_bike_temp)

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

# chk_temp(current_float_temp, max_bike_temp, min_bike_temp)

distance = config_data["bike_distance"]

def chk_bike_distance(distance, max_bike_distance):
    if distance <= max_bike_distance:
        return True
    else:
        return False

def chk_bike(temp, distance):
    if temp and distance:
        return True

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

print(response_data)