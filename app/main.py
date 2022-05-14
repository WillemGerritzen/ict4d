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
     return Response(data, mimetype='text/xml')


@app.route('/json')
def json():
    data = {"weather": "the weather is good"}
    return jsonify(data)

@app.route('/getdata/',methods = ['POST'])
def getdata():
    if not request.data:  
        return ('fail')
    student = request.get_json()

    #with open('file.txt','w') as f:
    #    f.write('success')

    print('_______________________________')
    print('success')
    print(student)
    return student

@app.route('/getcity/', methods=['POST'])
def getcity():
    if not request.data: 
        return ('fail')
    loc = request.get_json()
    city = loc['location']

    print(loc)
    return city

@app.route('/getweather/')
def getweather():
    # if not request.data:  
    #     return ('fail')
    # city = request.get_json()

    #with open('city.txt','r') as f:
    #    mycity = f.read() 
    #mycity = mycity.strip('\n')
    #city_num = g.get('city',None)

    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # load_weather = json.load(open(APP_ROOT))
    # with open(os.path.join(APP_STATIC_TXT, 'demo.json')) as f:
    #         load_weather = json.load(f)
    load_weather = {"coord": {"lon": -11, "lat": 14}, "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}], "base": "stations", "main": {"temp": 312.58, "feels_like": 310.95, "temp_min": 312.58, "temp_max": 312.58, "pressure": 1006, "humidity": 17, "sea_level": 1006, "grnd_level": 984}, "visibility": 10000, "wind": {"speed": 2.78, "deg": 133, "gust": 2.03}, "clouds": {"all": 0}, "dt": 1651241672, "sys": {"country": "ML", "sunrise": 1651213378, "sunset": 1651258772}, "timezone": 0, "id": 2455517, "name": "Kayes", "cod": 200}
    # for i in range(len(load_weather)):
    #     if i == city_num:
    mycity = load_weather['name']
    description = load_weather['weather'][0]['description']
    temperature = str(int(load_weather['main']['temp'] - 273.15))
    wind_speed = str(load_weather['wind']['speed'])
    humidity = str(load_weather['main']['humidity'])
    pressure = str(load_weather['main']['pressure'])

    weather_report = " is currently " + description + ". The temperature is " + temperature + " degrees Celsius. The wind speed is " + wind_speed + " kilometers per hour. The humidity is " + humidity + " percent. The air pressure is " + pressure + " hectopascal."
    data = {"weather": weather_report, "temp": int(load_weather['main']['temp'] - 273.15), "wind": load_weather['wind']['speed']}

    return jsonify(data)





