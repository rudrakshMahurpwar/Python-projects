from env import weatherapikey
import requests
import json

city = input("Enter the name of City: ")

url = f"http://api.weatherapi.com/v1/current.json?key={weatherapikey}&q={city}"

data = requests.get(url).json()

condition = data["current"]["condition"]["text"]
temp_c = data["current"]["temp_c"]


print(f"The Temperature of {city} is {condition}")
print(f"The Temperature of {city} is {temp_c} degree Celcius.")
