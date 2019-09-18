# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from SalesInfo import settings


class SalesinfoPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()
        print('数据库链接成功')

    def process_item(self, item, spider):
        try:
            for x in item:
                if item[x] == None:
                    item[x] = "无"
            thesql = "insert into a1688item_selloffer (title,company,price,sell,method,rebuy,address,subicon) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            thelist = (
            item['title'], item['company'], item['price'], item['sell'], item['method'], item['rebuy'], item['address'],
            item['subicon'])

            self.cursor.execute(thesql, thelist)

            print('事务插入成功')
            self.connect.commit()
        except Exception as error:
            print('插入错误', error)
        return item
