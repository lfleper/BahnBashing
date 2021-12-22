import scrapy

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://mobile.bahn.de/bin/mobil/query.exe/dox']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)
