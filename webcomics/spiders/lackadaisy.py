import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LackadaisySpider(CrawlSpider):
    name = 'lackadaisy'
    allowed_domains = ['lackadaisycats.com']
    start_urls = ['https://www.lackadaisycats.com/comic.php?comicdid=1']

    rules = (
        Rule(LxmlLinkExtractor(allow=r'comic\.php\?comicid=\d+', restrict_xpaths=('//div[@class="next"]/a/@href')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath('//img[@alt]').get()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print("Neues Item gefunden:")
        print(item['title'])
        return item
