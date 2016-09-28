#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as Q

def sessiontest():
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }

    login_url = 'http://login.solarzoom.com/login'

    data = {
        'username': 'abcd',
        'password': '123456',
        'submit': '登录'
    }

    # 获取参数
    r = session.get(login_url)
    for _ in Q(r.text).find('input[type="hidden"]'):
        data[Q(_).attr('name')] = Q(_).val()

    new = session.post(login_url, data)
    
    print(new.url)


if __name__ == '__main__':
    sessiontest()