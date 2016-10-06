#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as Q
import logger
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

session = requests.Session()


def getAllhrefsFromSql():
    conn = sqlite3.connect(DB_Helper.db_file)
    sqlstr = "select url from %s" % DB_Helper.PvNewsUrlSet_Table
    cursor = conn.execute(sqlstr)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    hrefList = [i[0] for i in values]
    return hrefList


def searchAllHrefs(item_type):
    newHrefs = set()
    hrefList = getAllhrefsFromSql()
    count = 1
    maxlen = len(pages)
    
    conn = sqlite3.connect(DB_Helper.db_file)
    print("开始载入页面中所有链接的数据")
    for page in pages:
        '''查询当前页面上 所有list_list中的href'''
        print("正在处理第%s/%s 页" % (count, maxlen))
        time.sleep(0.5)
        count += 1
        ObjUrl = BaseUrl + page
        bsObj = UrlUtility.getBsObjFromUrl(ObjUrl)
        
        try:
            newtable = bsObj.find("div", {'class': 'list_list'})
            newlist = newtable.find_all('a')
        except AttributeError as e:
            logger.logger.error("页面: %s  href列表 查询失败" % page)
        else:
            for item in newlist:
                checkhref = item.get_text()
                if not checkhref in hrefList:
                    newHrefs.add(checkhref)
            
            for href in newHrefs:
                insertSql = "insert into %s (url,type) values ('%s','%s' )" \
                            % (DB_Helper.PvNewsUrlSet_Table, href, item_type)
                try:
                    conn.execute(insertSql)
                except sqlite3.OperationalError:
                    print("插入地址出错 %s" % href)
            conn.commit()
    conn.close()


def searchAllPages(url, name):
    '''获得所有页面链接'''
    global pages
    ObjUrl = BaseUrl + url
    regular_str = r"\/%s\/index_*[0-9]*\.php" % name
    
    time.sleep(1)
    bsObj = UrlUtility.getBsObjFromUrl(ObjUrl)
    if bsObj is None:
        return
    
    links = bsObj.find_all('a', href=re.compile(regular_str))
    for link in links:
        if 'href' in link.attrs:
            newhref = link.attrs['href']
            if newhref not in pages:
                # 新页面
                pages.add(newhref)
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
    print('共有 %s页' % len(pages))
    
    searchAllHrefs(item_type)


if __name__ == '__main__':
    getDataByItem('多晶硅料')
