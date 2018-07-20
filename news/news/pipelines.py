# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import  codecs, sys
from datetime import date
import datetime
import time
import re
from scrapy.exceptions import DropItem

from contextlib import contextmanager
from news.models import News, db_connect, create_news_table
from sqlalchemy.orm import sessionmaker

import logging
_log = logging.getLogger(__name__)

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class NewsPipeline(object):
    def __init__(self):
        """
        json文件存储
        """
        filename = str(date.today()) + ".json"
        self.file = codecs.open('data/' + filename, 'w', encoding='utf-8')

        """
        db存储
        """
        engine = db_connect()
        create_news_table(engine)
        # 初始化对象属性Session为可调用对象
        self.Session = sessionmaker(bind=engine)

        """
        去重
        """
        self.cache_urls = []
        self.nowtime = datetime.datetime.now();

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        _log.info('open_spider[%s]....' % spider.name)
        session = self.Session()
        recent_news = session.query(News.m_url).filter(
            self.nowtime - News.m_public_time <= datetime.timedelta(days=2)).all()
        self.cache_urls = [t.m_url for t in recent_news]
        print(self.cache_urls)
        _log.info(self.cache_urls)

    def process_item(self, item, spider):
        """
        去重
        """
        if item['url'] in self.cache_urls:
            _log.info('[url exists!]url=%s' % item['url'])
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.cache_urls.append(item['url'])

        publishDate = str(item['publishTime'])
        """
        日期转换成时间戳
        """
        if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', publishDate):
            publishTime = int(time.mktime(time.strptime(publishDate, '%Y-%m-%d %H:%M:%S')))
        elif re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', publishDate):
            publishTime = int(time.mktime(time.strptime(publishDate, '%Y-%m-%d %H:%M')))

        item['publishTime'] = publishTime
        jtext = json.dumps(item['jtext'], ensure_ascii=False)
        news = News(m_title=item['title'],
                        m_json_text = jtext,
                        m_url=item['url'],
                        m_public_time=item['publishTime'],
                        m_from = 1,
                        m_site=item['site'])
        with session_scope(self.Session) as session:
            session.add(news)
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)

        return item

    def close_spider(self, spider):
        self.file.close()

