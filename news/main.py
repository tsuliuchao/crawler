#from scrapy import cmdline
#cmdline.execute("scrapy crawl sohunews".split())


import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from news.spiders.sohu_stars_news import SohuNewsSpider

if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)

    runner = CrawlerRunner(settings)
    runner.crawl(SohuNewsSpider)
    #runner.crawl(MySpider2)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run() #
    logging.info('all finished.')