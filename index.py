#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import time
from datetime import datetime

from bottle import (Bottle, HTTPResponse, request, response, run, json_dumps as dumps)

from getData import getDataSync, getShDataSync

app = Bottle()


@app.hook('after_request')
def enable_cors():
    print("after_request hook")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route("/", method=['GET', 'OPTIONS'])
def index():
    return "UP"


@app.post('/search')
def search():
    return HTTPResponse(body=dumps(
        ['all', 'sh', 'uttil times', 'gntotal', 'sustotal', 'deathtotal', 'curetotal', 'addcon', 'wjw_addsus',
         'adddeath', 'addcure', 'sh_value', 'sh_susNum', 'sh_cureNum', 'sh_deathNum', 'cn_chart_value',
         'cn_chart_susNum', 'cn_chart_cureNum', 'cn_chart_deathNum', 'sh_chart_value', 'sh_chart_susNum',
         'sh_chart_cureNum', 'sh_chart_deathNum', 'sh uttil times']),
        headers={'Content-Type': 'application/json'})


@app.post('/query')
def query():
    print(request.json)
    body = []
    all_data = getDataSync()
    sh_data = getShDataSync()
    time_stamp = int(round(time.time() * 1000))
    if request.json['targets'][0]['type'] == 'table':
        rows = []
        for data in all_data['list']:
            row = [data['name'], data['value'], data['susNum'], data['cureNum'], data['deathNum']]
            rows.append(row)
        sh_rows = []
        for data in sh_data['city']:
            row = [data['name'], data['conNum'], data['susNum'], data['cureNum'], data['deathNum']]
            sh_rows.append(row)
        bodies = {'all': [{
            "columns": [
                {"text": "省份", "type": "name"},
                {"text": "确诊", " type": "conNum"},
                {"text": "疑似", " type": "susNum"},
                {"text": "治愈", "type": "cureNum"},
                {"text": "死亡", "type": "deathNum"}
            ],
            "rows": rows,
            "type": "table"
        }],
            'sh': [{
                "columns": [
                    {"text": "省份", "type": "name"},
                    {"text": "确诊", " type": "value"},
                    {"text": "疑似", " type": "susNum"},
                    {"text": "治愈", "type": "cureNum"},
                    {"text": "死亡", "type": "deathNum"}
                ],
                "rows": sh_rows,
                "type": "table"
            }]}

        series = request.json['targets'][0]['target']
        body = dumps(bodies[series])
    else:
        for target in request.json['targets']:
            name = target['target']
            if name == 'gntotal':
                body.append({'target': 'gntotal', 'datapoints': [[all_data['gntotal'], time_stamp]]})
            if name == 'sustotal':
                body.append({'target': 'sustotal', 'datapoints': [[all_data['sustotal'], time_stamp]]})
            if name == 'curetotal':
                body.append({'target': 'curetotal', 'datapoints': [[all_data['curetotal'], time_stamp]]})
            if name == 'deathtotal':
                body.append({'target': 'deathtotal', 'datapoints': [[all_data['deathtotal'], time_stamp]]})
            if name == 'uttil times':
                body.append({'target': 'uttil times', 'datapoints': [[all_data['times'], time_stamp]]})
            if name == 'addcon':
                body.append({'target': 'addcon', 'datapoints': [[all_data['add_daily']['addcon'], time_stamp]]})
            if name == 'wjw_addsus':
                body.append({'target': 'wjw_addsus', 'datapoints': [[all_data['add_daily']['wjw_addsus'], time_stamp]]})
            if name == 'adddeath':
                body.append({'target': 'adddeath', 'datapoints': [[all_data['add_daily']['adddeath'], time_stamp]]})
            if name == 'addcure':
                body.append({'target': 'addcure', 'datapoints': [[all_data['add_daily']['addcure'], time_stamp]]})
            if name == 'cn_chart_value':
                historylist = all_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['cn_conNum'], timeStamp])
                body.append({'target': '确诊', 'datapoints': datapoints})
            if name == 'cn_chart_susNum':
                historylist = all_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['cn_susNum'], timeStamp])
                body.append({'target': '疑似', 'datapoints': datapoints})
            if name == 'cn_chart_cureNum':
                historylist = all_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['cn_cureNum'], timeStamp])
                body.append({'target': '治愈', 'datapoints': datapoints})
            if name == 'cn_chart_deathNum':
                historylist = all_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['cn_deathNum'], timeStamp])
                body.append({'target': '死亡', 'datapoints': datapoints})
            if name == 'sh uttil times':
                body.append({'target': 'uttil times', 'datapoints': [[sh_data['times'], time_stamp]]})
            if name == 'sh_value':
                body.append({'target': 'sh_value', 'datapoints': [[sh_data['contotal'], time_stamp]]})
            if name == 'sh_susNum':
                body.append({'target': 'sh_susNum', 'datapoints': [[sh_data['sustotal'], time_stamp]]})
            if name == 'sh_cureNum':
                body.append({'target': 'sh_cureNum', 'datapoints': [[sh_data['curetotal'], time_stamp]]})
            if name == 'sh_deathNum':
                body.append({'target': 'sh_deathNum', 'datapoints': [[sh_data['deathtotal'], time_stamp]]})
            if name == 'sh_chart_value':
                historylist = sh_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['conNum'], timeStamp])
                body.append({'target': '确诊', 'datapoints': datapoints})
            if name == 'sh_chart_susNum':
                historylist = sh_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['susNum'], timeStamp])
                body.append({'target': '疑似', 'datapoints': datapoints})
            if name == 'sh_chart_cureNum':
                historylist = sh_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['cureNum'], timeStamp])
                body.append({'target': '治愈', 'datapoints': datapoints})
            if name == 'sh_chart_deathNum':
                historylist = sh_data['historylist']
                datapoints = []
                for history in historylist:
                    his_time = '2020.{history}'.format(history=history['date'])
                    timeStamp = int(time.mktime(datetime.strptime(his_time, '%Y.%m.%d').timetuple())) * 1000
                    datapoints.append([history['deathNum'], timeStamp])
                body.append({'target': '死亡', 'datapoints': datapoints})
        body = dumps(body)

    return HTTPResponse(body=body, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=3000)
