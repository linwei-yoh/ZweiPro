#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
import re

import requests
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup

err_path = '../err.php'
nor_path = '../normal.php'
test_path = '../test.php'


def test1():
    page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    tree = html.fromstring(page.text)
    
    # 这将创建buyers的列表：
    buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    # 这将创建prices的列表：
    prices = tree.xpath('//span[@class="item-price"]/text()')
    
    print('Buyers: ', buyers)
    print('Prices: ', prices)


def test2():
    page = open(err_path, encoding='utf-8').read()
    tree = html.fromstring(page)
    tdlist = tree.xpath('//div[@class="bencandy_nr"]/table')[0]
    
    cleaner = Cleaner(style=True, scripts=True, remove_tags=['span', 'font', 'div'])
    tdlist = cleaner.clean_html(etree.tostring(tdlist))
    print(tdlist)
    tdlist = html.fromstring(page)
    df = pd.read_html(etree.tostring(tdlist), header=0)[0]
    print(df)


def test3():
    page = open(test_path, encoding='utf-8').read()
    tree = html.fromstring(page)
    print(tree.xpath("//text()"))
    # trlist = tree.xpath('//tr//span/text()')
    # print(trlist)


def test4():
    page = open(test_path, encoding='utf-8').read()
    # cleaner = Cleaner(style=True, scripts=True, remove_tags=['span', 'font', 'div'])
    # tdlist = cleaner.clean_html(page)
    bsObj = BeautifulSoup(page, 'lxml')
    print(bsObj)


def test5():
    page = open(test_path, encoding='utf-8').read()
    result = page.split('<tr>')[1:]
    
    for index in range(len(result)):
        print(result[index])


table1 = '../type1.txt'
table2 = '../type2.txt'
table3 = '../type3.txt'


def table1_pd():
    page = open(table1).read()
    bsObj = BeautifulSoup(page, 'lxml')
    
    trnode = bsObj.find('tr')
    div_first = trnode.find_all('td')
    print(len(div_first))
    
    for div in div_first:
        print(div.get_text())
    
    df = pd.read_html(page, header=0)[0]
    # print(df.columns[0]) # 表名
    
    # 加上.copy()可以避免警告 虽然都能正确设置值
    df2 = df.iloc[1:].copy()
    df2.columns = df.iloc[0].values
    print(df2)


def table2_pd():
    page = open(table3, encoding='utf-8').read()
    bsObj = BeautifulSoup(page, 'lxml')
    
    trnode = bsObj.find('tr')
    div_first = trnode.find_all('td')
    print(len(div_first))
    for div in div_first:
        print(div.get_text())
    
    df = pd.read_html(page, header=0)[0]
    
    df2 = df.iloc[1:, 0:-1]
    df2.columns = df.columns.delete(0)
    df2 = df2.append(df.iloc[0, 1:])
    
    # df2.insert(0, '产品', None)
    # df2['产品'] = df.iat[0, 0].replace(' ', '')
    df2 = df2.sort_index()
    print(df2)


if __name__ == '__main__':
    # p = re.compile(r"(?<=\d{1,2}'月'\d{2}'日'?)\w+(?='部分)")
    strpat = r'(?<=\d{1,2}%s\d{2}%s?)\w+(?=%s)' % ('月', '日', '部分')
    tarstr = '10月11日250W多晶硅电池组件部分厂家出厂含税报价'
    re.search(strpat, tarstr)
    # print(p.findall('one1two2three3four4'))
