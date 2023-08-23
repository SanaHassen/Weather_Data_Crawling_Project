from flask import Flask, request
from cassandra.cluster import Cluster
import json

api = Flask(__name__)
cluster = Cluster(['cassandra'])  
session = cluster.connect()
keyspace_name = "weather_db"
session.set_keyspace(keyspace_name)

@api.get('/weather')
def response_weather():
    city = request.args.get('city')
    search_query = """
    SELECT * FROM weather_table WHERE name=%s ALLOW FILTERING;
    """
    response = session.execute(search_query, [city])
    result = []
    for row in response: 
        result.append({
            'City name': row.name, 
            'weather': row.weather, 
            'description': row.description ,
            'temperature': row.temperature,
            'feels_like': row.feels_like ,
            'humidity': row.humidity ,
            'pressure': row.pressure 
        })  
    
    return json.dumps(result)

api.run(host='0.0.0.0', port=8080)
