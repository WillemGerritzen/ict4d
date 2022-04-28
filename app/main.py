import os
import requests
from flask import Flask, request, Response, jsonify
from app.db import conn
from app.get_weather_info import *
import json

app = Flask(__name__)

class MyResponse(Response):
    default_mimetype = 'text/xml'

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
     return data


@app.route('/json')
def json():
    data = {"weather": "the weather is good"}
    return jsonify(data)


@app.route('/', methods=['GET', 'POST'])
def add_to_db():
    cur = conn.cursor()

    data = request.get_json()

    location = data['location']
    date = data['applicable_date']
    state_name = data['weather_state_name']
    max_temp = data['max_temp']
    min_temp = data['min_temp']
    precipitation = data['precipitation']
    wind_speed = data['wind_speed']
    wind_direction = data['wind_direction_compass']
    air_pressure = data['air_pressure']

    cur.execute("""
            INSERT INTO weather (location, temperature, precipitation, wind_speed, wind_direction, air_pressure)
            VALUES (%s, %s, %s, %s, %s, %s) 
            """, (location, date, temperature, precipitation, wind_speed, wind_direction, air_pressure)
                )
    conn.commit()

    cur.close()

    return 'OK'








