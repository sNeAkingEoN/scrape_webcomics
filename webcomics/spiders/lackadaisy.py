import scrapy


class LackadaisySpider(scrapy.Spider):
    name = 'lackadaisy'
    allowed_domains = ['www.lackadaisycats.com']
    start_urls = ['http://www.lackadaisycats.com/']

    def parse(self, response):
        pass
