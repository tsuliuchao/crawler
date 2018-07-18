import scrapy
from scrapy import Request

class SohuNewsSpider(scrapy.Spider):
    name = "sohunews"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Upgrade-Insecure-Requests': 1,
        'Remote Address': '220.181.90.8:80',
    }

    start_urls = [
        "http://yule.sohu.com/stars_news.shtml",
    ]

    def start_requests(self):
        url = 'http://yule.sohu.com/stars_news.shtml'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        newsList = response.xpath('//div[@class="f14list"]/ul/li')
        for news in  newsList:
            try:
                print(news.xpath('./a/text()').extract()[0])
                print(news.xpath('./span[not(@class="star")]/text()').extract()[0])
            except:
                print("error")
