# -*- coding: utf-8 -*-
"""
Created on 2019/4/12 14:45
@Author  : zhangh
@File    : Python_weibo.py
@Project : PythonDemo
"""

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

client = MongoClient('192.168.11.131', 27017)
db = client['weibo']
collection = db['weibo']
max_page = 20

def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'referer': 'https://m.weibo.cn/u/2396481290',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2396481290',
        'containerid': '1076032396481290',
        'page': page
    }

    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        #print(response.status_code)
        #print(response.json())
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                weibo['created_at'] = item.get('created_at')
                yield weibo


if __name__ == '__main__':
    for page in range(1, max_page+1):
        json = get_page(page)
        #print(json)
        results = parse_page(json)
        for result in results:
            print(result)
            save_to_mongo(result)
