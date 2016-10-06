#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as Q
import DB_Helper
import sqlite3
import logger

# 硅料 21001 硅片 21002 电池片 21003 电池组件 21004

BaseUrl = 'http://db.solarzoom.com'
ObjUrl = "http://db.solarzoom.com/price_data/index.htm"
LoginUrl = 'http://login.solarzoom.com/login'

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


def getHrefSetByTypeWithForm(item, limit=None, delay=1, startpage=1):
    start_page = startpage

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
            if start_page >= (limit + startpage):
                return hrefset

        # 每个页面采集延迟1s 降低采集速度避免封杀与损耗服务器资源
        time.sleep(delay)


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
    s = session.post(LoginUrl, data=data, headers=headers)

    if s.url == 'http://login.solarzoom.com/login':
        print('登录Solarzoom失败')
        return False
    else:
        print('登录Solarzoom完成')
        return True


# def getDetailInfoToCSV(item, hrefset, delay=1):
#     if len(hrefset) == 0:
#         return
#
#     code = sel_item[item]
#     header = getheaderswithtype(code)
#     csvpath = os.path.join(savaPath, item + '.csv')
#
#     print("开始内链数据采集与保存: %s" % item)
#     for href in hrefset:
#         InfoUrl = BaseUrl + href
#         s = session.get(InfoUrl, headers=header)
#         bsObj = BeautifulSoup(s.text, 'lxml')
#
#         time.sleep(delay)
#
#         title = bsObj.find('div', {'class': 'ascout_quote_articletitle'}).get_text()
#         date = title[0:11]
#         table = bsObj.find('div', {'class': 'ascout_quote_articlecon'}).table
#         rows = table.tr.next_siblings
#
#         # uif-8 能正常的存入，但是EXCEL CVS会乱码
#         # 用gbk 能正确显示 但是会有报错
#         with open(csvpath, 'a', newline='', encoding='gbk') as csvFile:
#             writer = csv.writer(csvFile)
#             for row in rows:
#                 csvRow = [date]
#                 for cell in row.findAll(['td', 'th']):
#                     csvRow.append(cell.get_text().replace(u'\xa0', ' '))
#                 writer.writerow(csvRow)
#
#     print("数据获取完成")


def getDetailInfoToSqlite(item, hrefset, delay=1):
    if len(hrefset) == 0:
        print("没有新的数据")
        return

    print("开始内链数据采集与保存: %s" % item)
    code = sel_item[item]
    header = getheaderswithtype(code)
    conn = sqlite3.connect(DB_Helper.db_file)

    hrefsize = len(hrefset)
    hrefcount = 0
    for href in hrefset:
        InfoUrl = BaseUrl + href
        s = session.get(InfoUrl, headers=header)
        bsObj = BeautifulSoup(s.text, 'lxml')
        hrefcount += 1
        print("开始载入 %s / %s" % (hrefcount, hrefsize))
        
        time.sleep(delay)

        # 标题 日期获得
        title_ele = bsObj.find('div', {'class': 'ascout_quote_articletitle'})
        if title_ele is None:
            date = 'unknow'
            logger.logger.error("标题查询失败 Url:%s" % InfoUrl)
        else:
            date = (title_ele.get_text())[0:11]

        # 表 查询
        try:
            table_ele = bsObj.find('table')
            colnum = table_ele.find('tr')
        except AttributeError as e:
            logger.logger.error("表查询失败 Url:%s" % InfoUrl)
            continue

        # 表 列名获得
        col_list = []
        for col_name in colnum.find_all(['td', 'th']):
            col_list.append(col_name.get_text(strip=True))

        # 表 行获得
        rows = colnum.find_next_siblings('tr')

        # 将每行各个数据存入对应的字段中 并存储到sqlite中
        for row in rows:
            col_dir = {'date': date, '产品': None, '厂家': None, '价格': None, '涨跌': None, '单位': None, '含税': None}
            try:
                cells = row.find_all(['td', 'th'])
            except AttributeError as e:
                # 如果采用find_next_siblings()方法依旧会获得 navigateStrng则报错
                logger.logger.error("row find_all 失败 Url:%s" % InfoUrl)
                continue
    
            for i in range(len(cells)):
                col_dir[col_list[i]] = cells[i].get_text().replace(u'\xa0', ' ')
    
            if col_dir['产品'] == '' or col_dir['厂家'] == '':
                continue
            conn.execute("insert into %s (date,product,vender,price,change,unit,tax) "
                         "values ('%s','%s','%s','%s','%s','%s','%s')"
                         % (DB_Helper.SolarData_Table,
                            col_dir['date'], col_dir['产品'], col_dir['厂家'],
                            col_dir['价格'], col_dir['涨跌'], col_dir['单位'], col_dir['含税']))
        conn.commit()
        
    conn.close()
    print("数据保存完成")


def checkUrlInDB(hrefset):
    conn = sqlite3.connect(DB_Helper.db_file)
    newset = set()

    for href in hrefset:
        cursor = conn.execute("select count(*) from %s where url = '%s'" % (DB_Helper.SolarUrlSet_Table, href))
        count = cursor.fetchone()
        cursor.close()
        count = count[0]

        if count == 0:
            newset.add(href)
            conn.execute("insert into %s (url) values ('%s')" % (DB_Helper.SolarUrlSet_Table, href))
    conn.commit()
    conn.close()
    return newset


def ScrapingByItem(item, limit=None, delay=1, startpage=1):
    # 获得内链集合
    hrefset = getHrefSetByTypeWithForm(item, limit=limit, delay=delay, startpage=startpage)

    # 与数据库中已经记录的url比较
    newSet = checkUrlInDB(hrefset)

    # 获得详细数据
    getDetailInfoToSqlite(item, newSet, delay=delay)


def get_data_from_solarzoom(username, password):
    print("开始采集SolarZoom中的数据")

    # 账号登录
    if not accountLogin(username, password):
        return

    # 数据采集并保存
    # limit限制采集页数 默认无限制 直到采集完成
    # delay采集延迟 避免封杀 或损坏服务器资源 默认1s
    # 例子 ScrapingByItem('硅料', limit=1, startpage=47) 从47页开始获取1页
    ScrapingByItem('硅料')
    ScrapingByItem('硅片')
    ScrapingByItem('电池片')
    ScrapingByItem('电池组件')


if __name__ == '__main__':
    if not accountLogin('123456', '123456'):
        exit()
    
    code = sel_item['硅料']
    header = getheaderswithtype(code)
    testUrl = 'http://db.solarzoom.com/actual_price/article_575.htm'
    
    s = session.get(testUrl, headers=header)
    bsObj = BeautifulSoup(s.text, 'lxml')
    
    title_ele = bsObj.find('div', {'class': 'ascout_quote_articletitle'})
    if title_ele is None:
        date = 'unknow'
        logger.logger.error("标题查询失败")
    else:
        date = (title_ele.get_text())[0:11]
