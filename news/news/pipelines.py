# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import  codecs, sys
from datetime import date
import datetime

class NewsPipeline(object):
    def __init__(self):
        #filename = str(date.today() - datetime.timedelta(1)) + ".json"
        filename = str(date.today()) + ".json"
        self.file = codecs.open('data/' + filename, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
