# -*- encoding: utf-8 -*-

"""
Topic: 抓取搜狐娱乐滚动新闻
Desc :
"""
import time
import scrapy
from scrapy import Request
from news.items import NewsItem

import json
from datetime import date
import datetime
from news.settings import NEWS_CONTENT_INTERVAL_DAY

import logging
_log = logging.getLogger(__name__)

class SohuNewsSpider(scrapy.Spider):
    name = "sohunews"
    cache_url = []
    headers = {
        'Accept' : 'text/javascript, application/javascript, */*',
        'Accept-Encoding' : 'gzip, deflate',
        'Connection' : 'keep-alive',
        'Referer' : 'http://yule.sohu.com/roll/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With' : 'XMLHttpRequest',
    }

    def start_requests(self):
        paramDate = str(time.strftime("%Y%m%d", time.localtime(time.time() + NEWS_CONTENT_INTERVAL_DAY * 86400)))
        url = 'http://yule.sohu.com/_scroll_newslist/{}/news.inc'.format(paramDate)
        yield Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        responseBody = str(response.body_as_unicode()).replace("var newsJason =", "", 1).strip();
        responseBody = responseBody.replace('category:', '"category":', 1)
        responseBody = responseBody.replace('item:', '"item":', 1)
        try:
            obj = json.loads(responseBody)
            for item in obj['item']:

                url = item[2].strip()
                #url = 'https://www.sohu.com/a/241659063_178098?qq-pf-to=pcqq.group'
                """
                抓取页面排重
                """
                if url in self.cache_url:
                    continue
                else:
                    self.cache_url.append(url)

                if 'tv.sohu.com' in url:
                    continue
                elif 'yule.sohu.com' in url:
                    yield Request(str(url), callback=self.sub_parse_music, headers=self.headers)
                elif 'www.sohu.com/picture' in url:
                    yield Request(str(url), callback=self.sub_parse_pic, headers=self.headers)
                else:
                    yield Request(str(url), callback=self.sub_parse, headers=self.headers)
                #break
                time.sleep(0.5)
        except:
            _log.error(u'json内容错误.url=' + response.url)

    def sub_parse(self, response):

        """
        提取标题
        """
        title = response.xpath('//div[@class="text-title"]/h1')
        if not title:
            logging.error(u'[extrac error][标题]提取错误.url=' + response.url)
            return
        title = title.xpath('./text()').extract()[0]

        """
        提取发布日期
        """
        publishTime = response.xpath('//span[@id="news-time"]')
        if not publishTime:
            _log.error(u'[extract error][发布日期]提取错误.url=' + response.url)
            return
        publishTime = publishTime .xpath('./text()').extract()[0]

        """
        提取正文内容
        """
        jtext = []
        for p in response.xpath('//article[@id="mp-editor"]/p[not(@data-role="editor-name")]'):
            try:
                text = p.xpath('./text()')
                if text:
                    data = text.extract()[0]
                    if len(data) > 0:
                        jdata = {}
                        jdata['type'] = 'data'
                        jdata['text'] = data
                        jtext.append(jdata)
            except:
                _log.error(u'[extract error][正文]提取错误.url=' + response.url)

        item = NewsItem()
        item['title'] = title
        item['url'] = response.url
        item['publishTime'] = publishTime
        item['site'] = '八卦绯闻-搜狐娱乐'
        item['jtext'] = jtext
        yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理

    """
    音乐页面提取
    """
    def sub_parse_music(self, response):
        """
        提取标题
        """
        title = response.xpath('//h1[@itemprop="headline"]')
        if not title:
            _log.error(u'[extract error][标题]提取错误.url=' + response.url)
            return
        title = title.xpath('./text()').extract()[0]

        """
        提取发布日期
        """
        publishTime = response.xpath('//div[@id="pubtime_baidu"]')
        if not publishTime:
            _log.error(u'[extract error][发布日期]提取错误.url=' + response.url)
            return
        publishTime = publishTime .xpath('./text()').extract()[0]

        #print(publishTime)

        """
        提取来源
        """
        publisher = response.xpath('//span[@itemprop="publisher"]/span[@itemprop="name"]')
        if not publisher:
            _log.error(u'[extract error][抓取来源]提取错误.url=' + response.url)
            return
        publisher = publisher.xpath('./text()').extract()[0]

        #print(publisher)

        """
        提取正文内容
        """
        jtext = []
        for p in response.xpath('//div[@itemprop="articleBody"]/p[not(@class="text-pic")]'):
            try:
                data = p.xpath('./text()')
                if data:
                    data = data.extract()[0].strip()
                    if len(data) > 0:
                        jdata = {}
                        jdata['type'] = 'data'
                        jdata['text'] = data
                        jtext.append(jdata)
            except:
                _log.error(u'[extract error][正文]提取错误.url=' + response.url)
        item = NewsItem()
        item['title'] = title
        item['url'] = response.url
        item['publishTime'] = publishTime
        item['site'] = publisher
        item['jtext'] = jtext
        # print(item)
        yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理

    """
    图片页面提取
    """
    def sub_parse_pic(self, response):
        """
        提取标题
        """
        title = response.xpath('//h1[@id="article-title-hash"]')
        if not title:
            _log.error(u'[extract error][标题]提取错误.url=' + response.url)
            return
        title = title.xpath('./text()').extract()[0]
        # print(title)

        """
        提取发布日期
        """
        publishTime = response.xpath('//div[@class="info"]/span[@class="time"]')
        if not publishTime:
            _log.error(u'[extract error][发布日期]提取错误.url=' + response.url)
            return
        publishTime = publishTime .xpath('./text()').extract()[0]

        # print(publishTime)

        """
        提取来源
        """
        publisher = response.xpath('//div[@class="info"]/span[@class="name"]')
        if not publisher:
            f = open('log/errorUrl.txt', 'a')
            f.write('publisher extract error!\turl=' + response.url + '\n')
            return
        publisher = publisher.xpath('./text()').extract()[0]

        # print(publisher)

        """
        提取正文内容
        """
        jtext = []
        for p in response.xpath('//div[@class="pic-exp"]/div[@class="txt"]/p'):
            try:
                data = p.xpath('./text()')
                if data:
                    data = data.extract()[0].strip()
                    if len(data) > 0:
                        jdata = {}
                        jdata['type'] = 'data'
                        jdata['text'] = data
                        jtext.append(jdata)
            except:
                _log.error(u'[extract error][正文]提取错误.url=' + response.url)
        item = NewsItem()
        item['title'] = title
        item['url'] = response.url
        item['publishTime'] = publishTime
        item['site'] = publisher
        item['jtext'] = jtext
        # print(item)
        yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理
