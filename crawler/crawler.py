
from time import sleep
import requests
import json
from cassandra.cluster import Cluster
import uuid
from init_db import init_db


OPEN_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

OPEN_WEATHER_API_KEY = 'dd21a638583cc4d8d17e6e7b24b70348'

CITIES_FILE = 'city.list.json'

def get_city_weather(city_id: int):
  response =  requests.get(OPEN_WEATHER_API_URL, params={'id': city_id, 'appid': OPEN_WEATHER_API_KEY})
  return response.json()

def get_cities_ids():
  with open(CITIES_FILE, 'r') as f:
    all_cities = json.load(f)
    france_cities = [city['id'] for city in all_cities if city['country'] == "FR"]
    return france_cities

def write_to_cassandra(session, data_to_insert):
  insert_query = """
    INSERT INTO weather_table (id, name, weather, description, temperature, feels_like, humidity, pressure, country)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
  """
  session.execute(insert_query, (
  data_to_insert['id'],
    data_to_insert['name'],
    data_to_insert['weather'],
    data_to_insert['description'],
    data_to_insert['temperature'],
    data_to_insert['feels_like'],
    data_to_insert['humidity'],
    data_to_insert['pressure'],
    data_to_insert['country']
  ))


france_cities = get_cities_ids()
weather_info = []
for city_id in france_cities[0:100]:
  weather_info_by_city = get_city_weather(city_id)
  weather_info.append({
     'id': weather_info_by_city['id'],
      'name': weather_info_by_city['name'],
      'weather': weather_info_by_city['weather'][0]['main'],
      'description': weather_info_by_city['weather'][0]['main'],
      'temperature': weather_info_by_city['main']['temp'],
      'feels_like': weather_info_by_city['main']['feels_like'],
      'humidity': weather_info_by_city['main']['humidity'],
      'pressure': weather_info_by_city['main']['pressure'],
      'country': weather_info_by_city['sys']['country']
  })

cluster = Cluster(['cassandra'])  
session = cluster.connect()
keyspace_name = "weather_db"
init_db(session, keyspace_name)
session.set_keyspace(keyspace_name)

for info in weather_info:
  print('writing to DB: ', info['id'])
  write_to_cassandra(session=session, data_to_insert=info)

session.shutdown()
cluster.shutdown()