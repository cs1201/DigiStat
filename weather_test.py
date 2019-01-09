import requests
from requests_toolbelt.utils import dump
import json

city = "Swindon"
forecast_api_url = "https://api.openweathermap.org/data/2.5/forecast?"
appkey = "45e2590c09906f78a25e34ba0307ecd7"

forecast_request = requests.get(forecast_api_url, params={"q":city, "appid": appkey, "units": "metric", "cnt": "5"})
forecast_data = json.loads(forecast_request.content).get('list')
print(forecast_data)

# Over length of list, retreieve min and max temp, average these. and output

avg_min = 0
avg_max = 0

for timepoint in range(len(forecast_data)):

    temp_min = float(forecast_data[timepoint].get("main").get("temp_min"))
    temp_max = float(forecast_data[timepoint].get("main").get("temp_max"))

    avg_min = ( avg_min + temp_min ) / (timepoint+1)
    avg_max = ( avg_max + temp_max ) / (timepoint+1)

temp_curr= float(forecast_data[0].get("main").get("temp"))
weather_desc = forecast_data[0].get("weather")[0].get("description")

print(weather_desc)
print(temp_curr)


icon_code = forecast_data[0].get("weather")[0].get('icon')
# Download weather icon based on curren weather
base_icon_url = "http://openweathermap.org/img/w/"
icon_url = base_icon_url + icon_code + ".png"
icon_response = requests.get(icon_url)
if icon_response.status_code == 200:
    with open("curr_weather_icon.png", 'wb') as f:
        f.write(icon_response.content)
