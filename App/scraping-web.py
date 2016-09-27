#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

# 硅料 21001 硅片 21002 电池片 21003 电池组件 21004

ObjUrl = "http://db.solarzoom.com/price_data/index.htm"
LoginUrl = 'http://login.solarzoom.com/login'


def getheaderswithtype(code='21001'):
    referer_str = 'http://db.solarzoom.com/price_data/%s/index.htm' % code
    headers = {'Host': 'db.solarzoom.com',
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.112 '
                             'Safari/537.36',
               'Referer': referer_str,
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return headers


def getHrefSetByTypeWithForm(code='21001'):
    start_page = 50
    params = {'searchDate': '', 'productId': type, 'currentPage': str(start_page)}
    headers = getheaderswithtype(code)

    hrefset = set()
    while True:
        try:
            r = requests.post(ObjUrl, data=params, headers=headers)
        except requests.RequestException as e:
            print(e)
            return None
        else:
            # 获取当页内链
            bsObj = BeautifulSoup(r.text, 'lxml')
            formitem = bsObj.find("form", {"id": "listForm"})
            hrefTags = formitem.findAll("a", {"target": "_blank"})
            for hreftag in hrefTags:
                hrefset.add(hreftag.attrs['href'])

            print("已完成第%s页的采集" % start_page)
            # 检查是否还有下一页
            buttonlist = bsObj.findAll("input", {'name': 'button3', 'value': '下一页 >'})
            if len(buttonlist) == 0:
                return hrefset
            else:
                start_page += 1
            params['currentPage'] = start_page

            # 每个页面采集延迟1s 降低采集速度避免封杀与损耗服务器资源
            time.sleep(1)


def getLoginParam(username, password):
    r = requests.get(LoginUrl)
    bsObj = BeautifulSoup(r.text, 'lxml')
    lt = bsObj.find("input", {'name': 'lt'}).attrs['value']
    execution = bsObj.find("input", {'name': 'execution'}).attrs['value']
    eventId = bsObj.find("input", {'name': '_eventId'}).attrs['value']
    # button = bsObj.find("input", {'name': 'button'})
    params = {}
    params['username'] = username
    params['password'] = password
    params['lt'] = lt
    params['execution'] = execution
    params['_eventId'] = eventId
    params['button'] = "登录"
    return params


def getdatafromsolarzoom():
    params = getLoginParam("abcd", "1234")
    session = requests.Session()
    # 获得会话
    s = session.post(LoginUrl, params)


if __name__ == '__main__':
    print(getLoginParam())
