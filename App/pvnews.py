#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as Q
from logger import logger
import DB_Helper
import re
from bs4 import BeautifulSoup
import sqlite3
import time
import UrlUtility

LoginUrl = 'http://www.pvnews.cn/e/enews/index.php'
BaseUrl = 'http://www.pvnews.cn'

Url_dir = {'多晶硅料': '/yuanshengduojing/index.php',
           '硅片晶圆': '/guipianhangqing/index.php',
           '晶硅电池': '/dianchipian/index.php',
           '电池组件': '/dianchizujian/index.php'}

Name_dir = {'多晶硅料': 'yuanshengduojing',
            '硅片晶圆': 'guipianhangqing',
            '晶硅电池': 'dianchipian',
            '电池组件': 'dianchizujian'}

Type_dir = {'多晶硅料': '1',
            '硅片晶圆': '2',
            '晶硅电池': '3',
            '电池组件': '4'}

pages = set()
hrefs = set()

session = requests.Session()


def getAllhrefsFromSql():
    conn = sqlite3.connect(DB_Helper.db_file)
    sqlstr = "select url from %s" % DB_Helper.PvNewsUrlSet_Table
    cursor = conn.execute(sqlstr)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    hrefList = set(i[0] for i in values)
    return hrefList


def savehrefToSql(item_type):
    global hrefs
    newhref_count = 0
    hreflist = getAllhrefsFromSql()
    
    print("正在存储新的内链地址")
    conn = sqlite3.connect(DB_Helper.db_file)
    for href in hrefs:
        if not href in hreflist:
            insertSql = "insert into %s (url,type) values ('%s','%s' )" \
                        % (DB_Helper.PvNewsUrlSet_Table, href, item_type)
            conn.execute(insertSql)
            newhref_count += 1
    conn.commit()
    conn.close()
    print("内链地址更新完成 更新数量:%s" % newhref_count)


def searchAllPages(url, name):
    '''获得所有页面链接'''
    global pages
    global hrefs
    
    ObjUrl = BaseUrl + url
    regular_str = r"\/%s\/index_*[0-9]*\.php" % name
    pages.add(url)
    print("开始读取页面:%s" % len(pages))
    
    time.sleep(1)
    bsObj = UrlUtility.getBsObjFromUrl(ObjUrl)
    if bsObj is None:
        return

    try:
        newtable = bsObj.find("div", {'class': 'list_list'})
        newlist = newtable.find_all('a')
    except AttributeError as e:
        logger.error("页面: %s  href列表 查询失败" % url)
    else:
        for item in newlist:
            hrefs.add(item.attrs['href'])
    
    links = bsObj.find_all('a', href=re.compile(regular_str))
    for link in links:
        if 'href' in link.attrs:
            newhref = link.attrs['href']
            # 有新页面
            if newhref not in pages:
                searchAllPages(newhref, name)


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


def getDataByItem(item):
    global pages
    pages = set()
    
    item_type = Type_dir[item]
    item_url = Url_dir[item]
    item_name = Name_dir[item]
    print("%s :开始页面查询" % item)
    # 递归查询
    searchAllPages(item_url, item_name)

    # 存储内链地址
    savehrefToSql(item_type)


if __name__ == '__main__':
    bsobj = UrlUtility.getBsObjFromUrl('http://www.pvnews.cn/yuanshengduojing/2010-11-05/645.html')
    
    # 文章日期
    subtitle = bsobj.find('div', {'class': 'bencandy_ftitle'})
    article_date = subtitle.get_text(strip=True).split(' ', 1)[0]
    print(article_date)
    
    for child in bsobj.find('table').tr.find_next_siblings('tr'):
        print(child.get_text(" ", strip=True))
        print("-----------------------------------------------------")
