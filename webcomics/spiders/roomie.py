import scrapy
from ..items import ComicPageHtmlItem

class RoomieSpider(scrapy.Spider):
    name = 'roomie'
    allowed_domains = ['gogetaroomie.com']
    start_urls = ['https://www.gogetaroomie.com/']
    handle_httpstatus_list = [301]
    metadata_fields = ['strip_id', 'title', 'url', 'img_url', 'comment', 'publ_date']

    def parse(self, response):
        print("+++++++++++++++++++++++First URL downloaded:", response.url)
        link_to_first = response.xpath('//a[@class="cc-first"]/@href').get()
        print("~~~~~~~~~~~~~~~~~~~ URL to First Page:", link_to_first)
        yield scrapy.Request(url=link_to_first, callback=self.parse_page, dont_filter=False) # Warum auch immer! Achtung! Evtl. an anderen Stellen entfernen

    def parse_page(self, response):
        print("***************** Found page :)")
        link_to_next = response.xpath('//a[@class="cc-next"]/@href').get()
        print("***************** URL to Next Page:", link_to_next)
        page_item = self._create_page_item(response)
        return (scrapy.Request(url=link_to_next, callback=self.parse_page, dont_filter=False), page_item)

    def _create_page_item(self, response):
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = response.xpath('//div[@class="cc-publishtime"]/text()').get()
        item['title'] = response.url.split('/')[-1]
        item['url'] = response.url
        item['img_url'] = response.xpath('//img[@id="cc-comic"]/@src').get()
        item['comment'] = response.xpath('//div[@class="cc-newsarea"]').get()
        item['publ_date'] = response.xpath('//div[@class="cc-publishtime"]/text()').get()
        item['img_ext'] = item['img_url'].split('.')[-1]
        return item
        
