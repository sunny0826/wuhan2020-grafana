#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import json
import time

import requests


def get_header():
    '''get header

    :return: header
    '''
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'interface.sina.cn',
        'Referer': 'https://news.sina.cn/zt_d/yiqing0121',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    return headers


def req_get(headers, url):
    '''GET method

    :param headers: header
    :param url:  url
    :return: json result
    '''
    resp = requests.get(url, headers=headers)
    text = "".join(resp.text.rsplit()[1:-1])
    result = json.loads(text)
    return result['data']


def getDataSync():
    '''GET sync data

    :return: data
    '''
    headers = get_header()
    time_stamp = int(round(time.time() * 1000))
    url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json?_={timeStamp}&callback=Zepto1581561423453'.format(
        timeStamp=time_stamp)
    result = req_get(headers, url)
    return result


def getShDataSync():
    '''GET shanghai sync data

    :return: data
    '''
    headers = get_header()
    time_stamp = int(round(time.time() * 1000))
    url = 'https://interface.sina.cn/news/wap/historydata.d.json?province=shanghai&{timeStamp}&&callback=sinajp_15815768722009024855373127274'.format(
        timeStamp=time_stamp)
    result = req_get(headers, url)
    return result


if __name__ == '__main__':
    print(getShDataSync())
