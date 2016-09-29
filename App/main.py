#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DB_Helper
import solarzoom


if __name__ == '__main__':
    # 创建数据库
    DB_Helper.db_init()

    # 采集solarzoom数据
    solarzoom.get_data_from_solarzoom('grace_duo', '123456')
