# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class WatchesPipeline(object):
    def __init__(self):
        spiders = ['longines', 'tissort']
        try:
            self.conn = MySQLdb.connect(user='root', passwd='', host='localhost', db='watches',
                                        use_unicode=True, charset='utf8')
            self.cursor = self.conn.cursor()
            db_temp = "CREATE TABLE IF NOT EXISTS {}( idscrapedData INT NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
                      "retailer VARCHAR(200), store VARCHAR(200), address VARCHAR(200), email VARCHAR(200), " \
                      "phone VARCHAR(100), stock VARCHAR(100)) "

            execute = [db_temp.format(spider) for spider in spiders]

            for i in execute:
                self.cursor.execute(i)
                self.conn.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            raise e

    def process_item(self, item, spider):
        try:
            if 'longines_products' in spider.name:
                table_name = 'longines'
                self.spider_table(item, table_name)
            if 'tissort_products' in spider.name:
                table_name = 'tissort'
                self.spider_table(item, table_name)

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item

    def spider_table(self, item, table_name):
        self.cursor.execute(
            "INSERT INTO {} ( retailer, store, address, email, phone, stock) "
            "VALUES (%s, %s, %s, %s, %s, %s)".format(table_name),
            (item['retailer'],
             item['store_name'],
             item['address'],
             item['email'],
             item['phone'],
             item['stock']))
        self.conn.commit()