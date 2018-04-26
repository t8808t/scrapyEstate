# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy import log
import MySQLdb
import MySQLdb.cursors
import copy
class EstatePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                            host = "127.0.0.1",
                                            db="scrapydb",  # 数据库名
                                            user="root",  # 数据库用户名
                                            passwd="root",  # 密码
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset="utf8",
                                            use_unicode=False
                                            )

    def process_item(self, item, spider):
        asynItem = copy.deepcopy(item)
        query = self.dbpool.runInteraction(self._conditional_insert, asynItem)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tb, item):
        tb.execute("insert into estate (cjsj,scgpshsj,fwtybh,fczsh ,gplxrxm ,mdmc ,cqmc ,xzqhname,xqmc,jzmj,wtcsjg) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item["cjsj"],item["scgpshsj"],item["fwtybh"],item["fczsh"],item["gplxrxm"],item["mdmc"],item["cqmc"],item["xzqhname"],item["xqmc"],item["jzmj"],item["wtcsjg"]))
        #log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
