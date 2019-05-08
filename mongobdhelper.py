#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Defines a MongoOperator class and allows you to manipulate
the Mongodb Database.(insert, delete, update, select...)
'''

from pymongo import MongoClient, errors
from config import mongo

class MongoOperator(object):

    def __init__(self, **login):
        # connectin to test database:
        self.__db = MongoClient(login['host'], login['port'])[login['database']]
        self.__db.authenticate(login['user'], login['password'])





def get_mongodb_conn(choose, filter, flag):
    # 创建Connection时，指定host及port参数
    mongoClient = MongoClient(host=mongo[0], port=27017, username=mongo[1], password=mongo[2])
    db = mongoClient.attendance3  # 连接数据库

    results = ''
    if choose == 'users':
        results = db.users.find()  # 连接集合
    elif choose == 'records':
        if flag==1:
            results = db.records.find(filter)
        elif flag==0:
            results = db.records.find(filter).count()
    elif choose == 'signinrecords':
        results = db.signinrecords.find()
    else:
        print('collections is not right!')
    return results