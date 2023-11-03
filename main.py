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
max_wind_speed = config_data["max_wind_speed"]

ip = get('https://api.ipify.org').content.decode('utf8')

location_key = ""
api_key = "4A8s1R9XEApO2lZV3FseGqfV198SawHy"

url = f"http://dataservice.accuweather.com/locations/v1/cities/ipaddress?q={ip}&apikey={api_key}"

response = requests.get(url)

location_data = response.json()
location_key = location_data['Key']

print(location_key)

conditionsUrl = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"

conditionsResponse = requests.get(conditionsUrl)

conditions_data = conditionsResponse.json()

print(conditions_data)