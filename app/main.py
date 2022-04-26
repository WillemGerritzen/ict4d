import os

from flask import Flask, request
from db import conn

app = Flask(__name__)


@app.route('/', methods=['POST'])
def add_to_db():
    cur = conn.cursor()

    data = request.get_json()

    location = data['location']
    temperature = data['temperature']
    precipitation = data['precipitation']
    wind_speed = data['wind_speed']
    wind_direction = data['wind_direction']
    air_pressure = data['air_pressure']

    cur.execute("""
            INSERT INTO weather (location, temperature, precipitation, wind_speed, wind_direction, air_pressure)
            VALUES (%s, %s, %s, %s, %s, %s) 
            """, (location, temperature, precipitation, wind_speed, wind_direction, air_pressure)
                )
    conn.commit()

    cur.close()

    return 'OK'




