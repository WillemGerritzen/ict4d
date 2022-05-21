import os
import requests
from flask import Flask, request, Response, jsonify
import asyncio
from app.db import conn
import json
from app.connect_db import *
from app.get_weather_info import *
from flask import Flask, render_template, request
app = Flask(__name__)
from datetime import  datetime,timedelta


class MyResponse(Response):
    default_mimetype = 'text/xml'


@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'


@app.route('/initialize/')
def initialize():
    init_database()


@app.route('/insertLocationDate/', methods=['POST'])
def getcity():
    if not request.data:
        return ('fail')
    query = request.get_json()
    city = query['location']
    date = query['date']
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    id = postgres_manager.insert_data_locationDate(city, date)
    postgres_manager.closePostgresConnection()
    # insert into the locationDate Database, and return the query index
    return {'id': id}


@app.route('/getWeatherReport/', methods=['POST'])
def getWeatherReportNew():
    if not request.data:
        return ('fail')
    query = request.get_json()
    id = query['id']
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    row = postgres_manager.select_data_locationDate(id)
    load_weather = postgres_manager.select_data_day_weather(
        date=row[1], location=row[2])
    # load_weather=postgres_manager.select_data_day_weather(date='2022-05-04',location='New Delhi')

    postgres_manager.closePostgresConnection()
    data = {}
    data['description'] = load_weather[3]
    data['temperature_min'] = str(int(load_weather[4] - 273.15))
    data['temperature_max'] = str(int(load_weather[5] - 273.15))
    data['wind_speed'] = str(load_weather[6])
    data['humidity'] = str(load_weather[7])

    date = row[1]
    if date == "1":
        data['date'] = "today"
    elif date == "2":
        data['date'] = "tomorrow"
    else:
        data['date'] = "the day after tomorrow"

    # weather_report = " is currently " + description + ". The temperature is " + temperature_min+'~'+temperature_max + " degrees Celsius. The wind speed is " + \
    #     wind_speed + " kilometers per hour. The humidity is " + humidity + \
    #     " percent. "
    # data = {"weather": weather_report}
    return jsonify(data)


@app.route('/getWeatherReportFR/', methods=['POST'])
def getWeatherReportNewFR():
    if not request.data:
        return ('fail')
    query = request.get_json()
    id = query['id']
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    row = postgres_manager.select_data_locationDate(id)
    load_weather = postgres_manager.select_data_day_weather(
        date=row[1], location=row[2])
    # load_weather=postgres_manager.select_data_day_weather(date='2022-05-04',location='New Delhi')

    postgres_manager.closePostgresConnection()
    data = {}
    data['temperature_min'] = str(int(load_weather[4] - 273.15))
    data['temperature_max'] = str(int(load_weather[5] - 273.15))
    data['wind_speed'] = str(load_weather[6])
    data['humidity'] = str(load_weather[7])

    date = row[1]
    if date == "1":
        data['date'] = "aujourd'hui"
    elif date == "2":
        data['date'] = "demain"
    else:
        data['date'] = "le jour suivant"

    # weather_report = " is currently " + description + ". The temperature is " + temperature_min+'~'+temperature_max + " degrees Celsius. The wind speed is " + \
    #     wind_speed + " kilometers per hour. The humidity is " + humidity + \
    #     " percent. "
    # data = {"weather": weather_report}
    return jsonify(data)


@app.route('/getWeatherReport/<string:LDId>', methods=['GET'])
def getWeatherReport(LDId):
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    row = postgres_manager.select_data_locationDate(LDId)
    load_weather = postgres_manager.select_data_day_weather(
        date=row[1], location=row[2])
    # load_weather=postgres_manager.select_data_day_weather(date='2022-05-04',location='New Delhi')
    postgres_manager.closePostgresConnection()
    data = {}
    data['description'] = load_weather[3]
    data['temperature_min'] = str(int(load_weather[4] - 273.15))
    data['temperature_max'] = str(int(load_weather[5] - 273.15))
    data['wind_speed'] = str(load_weather[6])
    data['humidity'] = str(load_weather[7])

    # weather_report = " is currently " + description + ". The temperature is " + temperature_min+'~'+temperature_max + " degrees Celsius. The wind speed is " + \
    #     wind_speed + " kilometers per hour. The humidity is " + humidity + \
    #     " percent. "
    # data = {"weather": weather_report}
    return jsonify(data)


@app.route('/webForm', methods=('GET', 'POST'))
def locationDateForm():
    if request.method == 'GET':
        return render_template('locationDate.html')
    if request.method == 'POST':
        city = request.form['Location']
        days = request.form['date']
        date = (str(datetime.now().date()+timedelta(days=int(days)))[:10])
        cityList = ['Sikasso', 'Ségou', 'Kayes', 'Nara', 'Bamako']
        dateList = ['0','1','2','3','4','5','6']
        if city not in cityList or days not in dateList:
            return render_template('404.html')
        postgres_manager = PostgresBaseManager()
        postgres_manager.runServerPostgresDb()
        id = postgres_manager.insert_data_locationDate(city, date)
        row = postgres_manager.select_data_locationDate(id)
        load_weather = postgres_manager.select_data_day_weather(
            date=row[1], location=row[2])
        # load_weather=postgres_manager.select_data_day_weather(date='2022-05-04',location='New Delhi')
        postgres_manager.closePostgresConnection()
        data = {}
        data['description'] = load_weather[3]
        data['temperature_min'] = str(int(load_weather[4] - 273.15))
        data['temperature_max'] = str(int(load_weather[5] - 273.15))
        data['wind_speed'] = str(load_weather[6])
        data['humidity'] = str(load_weather[7])
        return render_template('result.html', city=city, home_url=request.host_url+'webForm', description=data['description'], temperature_min=data['temperature_min'],
                               temperature_max=data['temperature_max'], wind_speed=data['wind_speed'], humidity=data['humidity'])


@app.route('/alert', methods=('GET', 'POST'))
def Weatheralert():
    postgres_manager = PostgresBaseManager()
    info = postgres_manager.get_alert_info()
    return render_template('alert.html', info=info, home_url=request.host_url+'alert')


if __name__=='__main__':
    app.run()