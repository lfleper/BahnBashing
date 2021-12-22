# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bahn_bashing.spider import spider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(spider.Spider)
process.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
