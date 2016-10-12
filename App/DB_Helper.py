#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

db_name = 'scraping.db'
db_path = '../DataBase'
db_file = '../DataBase/scraping.db'

SolarUrlSet_Table = "Solar_Url"
SolarData_Table = 'Solar_Data'

PvNewsUrlSet_Table = 'PvNews_Url'
PvNewsData_Table = 'PvNews_Item'

Create_SolarUrlSet_Sql = 'create table %s (' \
                         'Id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                         'url text not null UNIQUE ON CONFLICT IGNORE);' \
                         % SolarUrlSet_Table

Create_SolarData_Sql = 'create table %s (' \
                       'Id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                       'date text not null,' \
                       'product text not null,' \
                       'vender text not null,' \
                       'price text,' \
                       'change text,' \
                       'unit text,' \
                       'tax text,' \
                       ' UNIQUE (date, product,vender) ON CONFLICT IGNORE);' \
                       % SolarData_Table

Create_PvNewsUrlSet_Sql = "create table %s (" \
                          "Id INTEGER PRIMARY KEY AUTOINCREMENT," \
                          "url text not null UNIQUE ON CONFLICT IGNORE," \
                          "type text not null default '1'," \
                          "mark integer default 0);" \
                          % PvNewsUrlSet_Table

Create_PvNewsData_Sql = "create table %s (" \
                        "Id INTEGER PRIMARY KEY AUTOINCREMENT," \
                        "date text not null," \
                        "category text not null," \
                        "vender text not null," \
                        "unit text not null," \
                        "value text," \
                        "change text," \
                        "output text," \
                        "remark text," \
                        "UNIQUE (date, category,vender) ON CONFLICT IGNORE);" \
                        % PvNewsData_Table

dict_sql = {SolarUrlSet_Table: Create_SolarUrlSet_Sql,
            SolarData_Table: Create_SolarData_Sql,
            PvNewsUrlSet_Table: Create_PvNewsUrlSet_Sql,
            PvNewsData_Table: Create_PvNewsData_Sql}


def CreateTable(dbpath, tablename):
    if tablename is None or dbpath is None:
        print('数据库路径或者表名不能为None')
        return False

    sqlstr = dict_sql[tablename]

    try:
        conn = sqlite3.connect(dbpath)
        conn.execute(sqlstr)
    except sqlite3.OperationalError as e:
        print('表: %s链接正常' % tablename)
    else:
        print('表: %s创建成功' % tablename)
    finally:
        conn.close()


def isTableExists(dbpath, tablename):
    if tablename is None or dbpath is None:
        return False

    sqlstr = "select count(*) from sqlite_master " \
             "where type = '%s' and name = '%s'" \
             % ('table', tablename)

    conn = sqlite3.connect(dbpath)
    cursor = conn.execute(sqlstr)
    count = cursor.fetchone()
    cursor.close()
    conn.close()

    count = count[0]
    if count == 0:
        return False
    else:
        return True


def db_init():
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    if not os.path.isfile(db_file):
        sqlite3.connect(db_file)

    # if not isTableExists(db_file, SolarUrlSet_Table):
    CreateTable(db_file, SolarUrlSet_Table)

    # if not isTableExists(db_file, SolarData_Table):
    CreateTable(db_file, SolarData_Table)

    CreateTable(db_file, PvNewsUrlSet_Table)
    # CreateTable(db_file, PvNewsData_Table) # 不再需要

    print('创建数据库 完成')


if __name__ == '__main__':
    db_init()
