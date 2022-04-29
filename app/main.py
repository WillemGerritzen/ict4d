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
    if not request.data:  # 检测是否有数据
        return ('fail')
    student = request.get_json()

    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    # student_json = json.loads(student)
    # 把区获取到的数据转为JSON格式。
    with open('file.txt','w') as f:
        f.write('success')

    print('_______________________________')
    print('success')
    print(student)
    return student

@app.route('/getcity/', methods=['POST'])
def getcity():
    if not request.data:  # 检测是否有数据
        return ('fail')
    city = request.get_json()

    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    # student_json = json.loads(student)
    # 把区获取到的数据转为JSON格式。
    with open('city.txt','w') as f:
        f.write('success')

    print('_______________________________')
    print('success')
    print(city)
    return city







