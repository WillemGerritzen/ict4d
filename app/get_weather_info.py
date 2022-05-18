import requests
import pandas as pd
from app.connect_db import *
from datetime import date,timedelta

APIKEY = 'e278b3cd7d40437755cf3f4a91bbd0d3'
BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall'
GEO_URL = 'http://api.openweathermap.org/geo/1.0/direct?'


def get_location(query):
    """
    get location id
    """
    r = requests.get(GEO_URL, params={
                     'q': query, 'country code': 'MLI', 'appid': APIKEY})
    data = r.json()
    print(data)
    if len(data):
        print('location found')
        location = {}
        location['lat'] = data[0]['lat']
        location['lon'] = data[0]['lon']
        return location
    else:
        print('no '+query+' location found')
        return -1


def get_weather(query):
    """
    get weather data
    """
    location = get_location(query)
    if location != -1:
        r = requests.get(BASE_URL, params={
                         'lat': location['lat'], 'lon': location['lon'], 'exclude': 'houryly,current,minutely,alerts', 'appid': APIKEY})
        data = r.json()
        result = {}
        result['location'] = query
        result['weather'] = []
        now = date.today()
        dayNumber = now

        for day_weather in data['daily']:
            result['weather'].append({
                'date': dayNumber,
                'main': day_weather['weather'][0]['main'],
                'description': day_weather['weather'][0]['description'] ,
                'temp_min': round(day_weather['temp']['min'], 2),
                'temp_max': round(day_weather['temp']['min'], 2),
                'wind_speed': round(day_weather['wind_speed'], 2),
                'humidity': round(day_weather['humidity'], 2)
            })
            dayNumber = dayNumber + timedelta(days=1)
        return result

def init_database():
    cityList = ['Sikasso', 'Ségou', 'Kayes', 'Nara', 'Bamako']
    df_Result = pd.DataFrame(columns=['date','location', 'main', 'description', 'temp_min','temp_max','wind_speed','humidity'])
    conn = PostgresBaseManager().engine
    for city in cityList:
        a = get_weather(city)
        print(a['weather'])
        df = pd.DataFrame(a['weather'])
        df['location'] = a['location']
        df_Result =df_Result.append(df)

    df_Result.to_sql(
        "day_weather",  # table name
        con=conn,
        if_exists='replace', #every time call is a new database
        index=False  # In order to avoid writing DataFrame index as a column
    )
    print(df_Result)
