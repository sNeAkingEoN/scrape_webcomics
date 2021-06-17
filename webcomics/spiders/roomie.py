import scrapy
from ..items import ComicPageHtmlItem
from .base_spiders import FromStartSpider

class RoomieSpider(FromStartSpider):
    name = 'roomie'
    allowed_domains = ['gogetaroomie.com']
    start_urls = ['https://www.gogetaroomie.com/']
    metadata_fields = ['strip_id', 'title', 'url', 'img_url', 'comment', 'publ_date']

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

    def _find_first(self, response):
        return response.xpath('//a[@class="cc-first"]/@href').get()

    def _find_next(self,response):
        return response.xpath('//a[@class="cc-next"]/@href').get()

        
