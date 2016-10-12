#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DB_Helper
import solarzoom
import pvnews

if __name__ == '__main__':
    # 创建数据库
    DB_Helper.db_init()

    # 采集solarzoom数据
    solarzoom.get_data_from_solarzoom('abcdefg', '123456')

    # 采集pvnews数据
    pvnews.get_data_from_pvnews('abcdefg', '123456')
