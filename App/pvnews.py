#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as Q
import Utility
import DB_Helper

LoginUrl = 'http://www.pvnews.cn/e/enews/index.php'

Url_dir = {'多晶硅料': "http://www.pvnews.cn/yuanshengduojing/",
           '硅片晶圆': 'http://www.pvnews.cn/guipianhangqing/',
           '晶硅电池': 'http://www.pvnews.cn/dianchipian/',
           '电池组件': 'http://www.pvnews.cn/dianchizujian/'}

session = requests.Session()

'''
POST http://www.pvnews.cn/e/enews/index.php
ecmsfrom:
enews:login
username:123456
password:122345
Submit:登录
'''


def getLoginParam(username, password):
    data = {'username': None, 'password': None, 'Submit': '登录'}
    
    data['ecmsfrom'] = ''
    data['enews'] = 'login'
    data['username'] = username
    data['password'] = password
    
    return data


def accountLogin(username, password):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/49.0.2623.112 '
                   'Safari/537.36'}
    
    data = getLoginParam(username, password)
    s = session.post(LoginUrl, data=data, headers=headers)
    
    if len(s.cookies) == 0:
        print("登录失败")
        return False
    else:
        print("登录完成")
        return True


if __name__ == '__main__':
    if not accountLogin('abcdefg', '123456'):
        exit()
    
    testUrl = 'http://www.pvnews.cn/yuanshengduojing/2016-09-29/162644.php'
    s = session.get(testUrl)
    bsObj = BeautifulSoup(s.text, 'lxml')
    
    try:
        table_ele = bsObj.find('div', {'class': 'bencandy_nr'}).table
        rows = table_ele.tr.find_next_siblings('tr')
    except AttributeError as e:
        print("页面崩溃 或者 也是不对")
    else:
        for row in rows:
            print(row.get_text('|', strip=True))
            
            # 厂家|备注|万元/吨|涨/跌
            # 福建明溪中硅科技有限公司|-|8|-
            # 福建亿田硅业有限公司|-|8|-
            # 上海普罗新能源有限公司|-|7.5|-
            # 宁夏银星多晶硅有限责任公司|-|8.5|-
            # 南阳迅天宇硅品有限公司|-|7.5|-
            # 济南天琴硅业有限公司|-|8.5|-
            # 佳科太阳能硅（厦门）有限公司|-|8.5|-
