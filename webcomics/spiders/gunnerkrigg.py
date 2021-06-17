import scrapy
from ..items import ComicPageHtmlItem
from .base_spiders import FromStartSpider

class GunnerkriggSpider(FromStartSpider):
    name = 'gunnerkrigg'
    allowed_domains = ['gunnerkrigg.com']
    start_urls = ['https://www.gunnerkrigg.com']
    metadata_fields = ['strip_id', 'url', 'img_url', 'comment', 'publ_date']
    domain = start_urls[0]
    max_strip_digits = 4

    def _create_page_item(self, response):
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = response.url.split('=')[-1]
        item['title'] = None
        item['url'] = response.url
        item['img_url'] = self.domain + response.xpath('//img[@class="comic_image"]/@src').get()
        item['comment'] = response.xpath('//div[@class="content"]/p').get()
        item['publ_date'] = response.xpath('//div[@class="content"]/a[@class="important"]/following-sibling::text()').get()
        item['img_ext'] = item['img_url'].split('.')[-1]
        return item

    def _find_first(self, response):
        return self.domain + '/' + response.xpath('//img[@src="/images/first_a.jpg"]/parent::a/@href').get()

    def _find_next(self,response):
        return self.domain + '/' + response.xpath('//img[@src="/images/next_a.jpg"]/parent::a/@href').get()

        
