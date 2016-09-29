#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

login_url = 'http://www.pvnews.cn/e/member/login/'
item_url1 = "http://www.pvnews.cn/yuanshengduojing/"

session = requests.Session()


def pvnew_test():
    r = requests.get(item_url1)
    r.encoding = 'utf-8'
    Objbs = BeautifulSoup(r.text, 'lxml')
    titlelist = Objbs.find('div', {'class', 'list_list'})
    print(titlelist)


def login_test():
    r = requests.get(login_url)
    print(r.text)


# def accountLogin(username, password):
#     (data, reqcookie) = getLoginParam(username, password)
#     headers = getLoginHeaders(reqcookie)
#     session.post(LoginUrl, data=data, headers=headers)

if __name__ == '__main__':
    login_test()
