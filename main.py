import datetime
import json
import requests
from requests import get

print("starting Tracefy© weather checker")

# get configurable preference data from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

max_bike_distance = config_data["max_bike_distance"]
max_bike_temp = config_data["max_bike_temp"]
min_bike_temp = config_data["min_bike_temp"]

ip = get('https://api.ipify.org').content.decode('utf8')

location_key = ""
api_key = "4A8s1R9XEApO2lZV3FseGqfV198SawHy"

url = f"http://dataservice.accuweather.com/locations/v1/cities/ipaddress?q={ip}&apikey={api_key}"

response = requests.get(url)

location_data = response.json()
location_key = location_data['Key']

# print(location_data)

conditionsUrl = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"

conditionsResponse = requests.get(conditionsUrl)

conditions_data = conditionsResponse.json()

# print(conditions_data)

current_weather = conditions_data[0]['WeatherText']
current_weather_ic = conditions_data[0]['WeatherIcon']
current_temp = conditions_data[0]['Temperature']['Metric']['Value']
current_float_temp = float(current_temp)
lat = location_data['GeoPosition']['Latitude']
lon = location_data['GeoPosition']['Longitude']

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

distance = '1km'

def chk_bike_distance(distance, max_bike_distance):
    if distance <= max_bike_distance:
        return True
    else:
        return False

def chk_bike(temp, distance):
    if temp and distance:
        return True

save_date = datetime.date.today()

temp = chk_temp(current_float_temp, max_bike_temp, min_bike_temp)
bike_distance = chk_bike_distance(distance, max_bike_distance)

response_data = {
    "Temprature": current_temp,
    "icon": current_weather_ic,
    "bikeable": chk_bike(temp, bike_distance),
    "Lat": lat,
    "Lon": lon,
    "Saved_at": save_date,
}

print(response_data)