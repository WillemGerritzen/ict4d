import os
import requests
from flask import Flask, request, Response, jsonify
from app.db import conn
from app.get_weather_info import *
import json

app = Flask(__name__)

#class MyResponse(Response):
#    default_mimetype = 'text/xml'

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


@app.route('/city')
def add_to_db():

    CITY = "Sikasso"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "ab75fb5cfed8a375955e5dc6a951438c"
    # upadting the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    response = requests.get(URL)

    if response.status_code == 200:
        #get json data
        data = response.json()
        main = data['main']
        #wea
        #temperature
        
        city_data = {"weather": "Error in the HTTP request"}

    return jsonify(city_data)








