# --encoding:utf-8--
#
import hashlib
import re

import pymysql
from config import *

class MySQLHelper:
    myVersion = 0.1

    def __init__(self, host, user, password, charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.password)
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print('MySql Error : %d %s' % (e.args[0], e.args[1]))

    def setDB(self, db):
        try:
            self.conn.select_db(db)
        except pymysql.Error as e:
            print('MySql Error : %d %s' % (e.args[0], e.args[1]))

    def deal(self, sql):
        try:
            self.cursor.execute(sql)
            self.commit()  # 命令需要提交
        except pymysql.Error as e:
            print('MySql Error: %s SQL: %s' % (e, sql))

    def queryAll(self, sql, return_results):
        try:
            self.deal(sql)
            if return_results:
                results = self.cursor.fetchall()
                return results
        except pymysql.Error as e:
            print('MySql Error: %s SQL: %s' % (e, sql))


    def getLastInsertRowId(self):
        return self.cursor.lastrowid

    def getRowCount(self):
        return self.cursor.rowcount

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # def turncateTable(self, tableName):
    #     sql = "turncate table {}".format(tableName)
    #     try:
    #         self.cursor.execute(sql)
    #         self.commit()
    #     except pymysql.Error as e:
    #         self.conn.rollback()
    #         print('MySql Error: %s SQL: %s' % (e, sql))
    #     finally:
    #         self.close()

class DealTable:

    helper = MySQLHelper(host=mysql[0], user=mysql[1], password=mysql[2])  # 创建对象
    helper.setDB(db=mysql[3])  # 选择对象

    # def turncate_Table(self, tableName):
    #     '''清空数据'''
    #     self.helper.turncateTable(tableName)

    def deal_table(self, sql):
        self.helper.deal(sql)

    def get_data(self, sql, return_results):
        return self.helper.queryAll(sql, return_results)


    def get_md5_value(self, data):
        my_md5_Digest = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
        return my_md5_Digest

    def check_if_exist(self,single_info, insert_sql, check_sql, delete_sql):
        '''检查数据是否存在，不存在则插入'''
        check_results = self.helper.queryAll(sql=check_sql, return_results=1)  # 查询出勤记录是否在表中
        if check_results == ():  # 如果某条记录不存在，则插入数据
            # print(check_results)
            self.helper.deal(sql=insert_sql)
            # print(insert_sql)
        else:
            md5_1 = self.get_md5_value(str(check_results[0]))
            md5_2 = self.get_md5_value(str(single_info))
            if md5_1 != md5_2:
                self.helper.deal(sql=delete_sql)  # 删除
                self.helper.deal(sql=insert_sql)  # 插入新数据


    def table_exists(self, table_name):
        """这个函数用来判断表是否存在"""
        sql = "show tables;"
        tables = [self.helper.queryAll(sql, return_results=1)]

        table_list = re.findall("(\'.*?\')", str(tables))
        table_list = [re.sub("\'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0



# if __name__ = '__main__':
