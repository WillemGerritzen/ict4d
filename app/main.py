import os

from flask import Flask, request, Response
from app.db import conn
from app.get_weather_info import *
import json

app = Flask(__name__)


@app.route('/')
def hello():

    return 'Welcome to My Watchlist!'

@app.route('/xml')
def xml():
     data = """<?xml version="1.0" encoding="UTF-8"?>
    <vxml version = "2.1" >
    <form>
    <block>
    <prompt>
    Hello World!
    </prompt>
    </block>
    </form>
    </vxml>
             """
     return Response(data, mimetype='text/xml')


@app.route('/json')
def json():
    data = {"weather": "the weather is good"}
    return Response(json.dumps(data), mimetype='json')

@app.route('/db', methods=['POST'])
def add_to_db():
    cur = conn.cursor()

    data = get_weather('delhi', 4)
    print(data)

    for i in data['weather']:
        location = data['location']
        pred_date = i['date']
        temperature = i['the_temp']
        weather_state = i['weather_state_name']
        wind_speed = i['wind_speed']
        wind_direction = i['wind_direction']
        humidity = i['humidity']

        cur.execute("""
                INSERT INTO weather (location, pred_date, temperature, weather_state, wind_speed, wind_direction, humidity)
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                """, (location, pred_date, temperature, weather_state, wind_speed, wind_direction, humidity)
                    )
        conn.commit()

        cur.close()

    return 'OK'

# add_to_db()




