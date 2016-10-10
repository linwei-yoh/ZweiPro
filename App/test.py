#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys

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


if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    page = open(err_path, encoding='utf-8').read()
    bsObj = BeautifulSoup(page, 'lxml')
    tablenode = bsObj.find('div', {'class': 'bencandy_nr'}).table
    df = pd.read_html(str(tablenode), header=0)[0]
    print(df)
