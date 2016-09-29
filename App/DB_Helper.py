#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

db_name = 'scraping.db'
db_path = '../DataBase'
db_file = '../DataBase/scraping.db'

SolarUrlSet_Table = "Solar_Url"
SolarData_Table = 'Solar_Data'

Create_SolarUrlSet_Sql = 'create table %s (' \
                         'Id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                         'url text not null UNIQUE ON CONFLICT IGNORE);' \
                         % SolarUrlSet_Table

Create_SolarDate_Sql = 'create table %s (' \
                       'Id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                       'date text not null,' \
                       'product text not null,' \
                       'vender text not null,' \
                       'price text,' \
                       'change text,' \
                       'unit text,' \
                       'tax text);' \
                       % SolarData_Table

dict_sql = {SolarUrlSet_Table: Create_SolarUrlSet_Sql,
            SolarData_Table: Create_SolarDate_Sql}


def CreateTable(dbpath, tablename):
    if tablename is None or dbpath is None:
        print('数据库路径或者表名不能为None')
        return False

    sqlstr = dict_sql[tablename]

    try:
        conn = sqlite3.connect(dbpath)
        conn.execute(sqlstr)
    except sqlite3.OperationalError as e:
        print(e)
        print('表: %s已经存在' % tablename)
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

    print('创建数据库 完成')


#
# def db_test():
#     href = "/actual/2102.html"
#     conn = sqlite3.connect(db_file)
#     cursor = conn.execute("select count(*) from %s where url = '%s'" % (SolarUrlSet_Table, href))
#
#     count = cursor.fetchone()
#     cursor.close()
#     count = count[0]
#
#     if count == 0:
#         conn.execute("insert into %s values ('%s')" % (SolarUrlSet_Table, href))
#
#     conn.commit()
#     conn.close()


if __name__ == '__main__':
    db_init()
