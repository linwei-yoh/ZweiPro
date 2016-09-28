#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as Q

# 硅料 21001 硅片 21002 电池片 21003 电池组件 21004

BaseUrl = 'http://db.solarzoom.com'
ObjUrl = "http://db.solarzoom.com/price_data/index.htm"
LoginUrl = 'http://login.solarzoom.com/login'

savaPath = '../SolarZoomData'

sel_item = {'硅料': '21001', '硅片': '21002', '电池片': '21003', '电池组件': '21004'}
session = requests.Session()


def getheaderswithtype(code):
    referer_str = 'http://db.solarzoom.com/price_data/%s/index.htm' % code
    headers = {'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.112 '
                             'Safari/537.36',
               'Referer': referer_str,
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return headers


def getHrefSetByTypeWithForm(item, limit=None):
    start_page = 1

    code = sel_item[item]
    headers = getheaderswithtype(code)
    params = {'searchDate': '', 'productId': code, 'currentPage': str(start_page)}

    hrefset = set()
    print("开始内链采集: " + item)
    while True:
        s = session.post(ObjUrl, data=params, headers=headers)

        # 获取当页内链
        bsObj = BeautifulSoup(s.text, 'lxml')
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

        if limit is not None:
            if start_page > limit:
                return hrefset

        # 每个页面采集延迟1s 降低采集速度避免封杀与损耗服务器资源
        time.sleep(2)


def getLoginParam(username, password):
    data = {'username': None, 'password': None, 'submit': '登录'}

    r = requests.get(LoginUrl)

    # 获取参数
    for _ in Q(r.text).find('input[type="hidden"]'):
        data[Q(_).attr('name')] = Q(_).val()
    data['username'] = username
    data['password'] = password

    # 获取用于heards的cookie
    cookie = r.cookies.get_dict()
    cookie_jesion = 'JSESSIONID=%s' % cookie['JSESSIONID']
    reqcookie = {'Cookie': cookie_jesion}

    return data, reqcookie


def getLoginHeaders(reqcookie):
    headers = {'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.112 '
                             'Safari/537.36',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    headers.update(reqcookie)
    return headers


def accountLogin(username, password):
    (data, reqcookie) = getLoginParam(username, password)
    headers = getLoginHeaders(reqcookie)
    session.post(LoginUrl, data=data, headers=headers)


def getDetailInfo(item, hrefset):
    if hrefset is None:
        return

    code = sel_item[item]
    csvpath = os.path.join(savaPath, item + '.csv')
    header = getheaderswithtype(code)

    print("开始保存数据到CSV")
    for href in hrefset:
        InfoUrl = BaseUrl + href
        s = session.get(InfoUrl, headers=header)
        bsObj = BeautifulSoup(s.text, 'lxml')

        title = bsObj.find('div', {'class': 'ascout_quote_articletitle'}).get_text()
        date = title[0:11]

        table = bsObj.find('div', {'class': 'ascout_quote_articlecon'}).table
        rows = table.tr.next_siblings

        with open(csvpath, 'a', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for row in rows:
                csvRow = [date]
                for cell in row.findAll(['td', 'th']):
                    csvRow.append(cell.get_text())
                writer.writerow(csvRow)

    print("数据保存完成")


def ScrapingByItem(item, limit=None):
    hrefset = getHrefSetByTypeWithForm(item, limit=limit)
    getDetailInfo(item, hrefset)


def get_data_from_solarzoom(username, password):
    print("开始采集SolarZoom中的数据")

    # 账号登录
    accountLogin(username, password)
    print('登录完成')

    # 数据采集并保存
    ScrapingByItem('硅料', limit=2)


if __name__ == '__main__':
    if not os.path.exists(savaPath):
        os.makedirs(savaPath)
    get_data_from_solarzoom('abcdefg', '123456')
