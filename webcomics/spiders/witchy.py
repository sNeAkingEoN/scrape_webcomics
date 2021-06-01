import os.path
import re
import scrapy
from .base_spiders import FromArchiveSpider
from ..items import ComicPageHtmlItem, ComicCanvasImageItem
from pathlib import Path
from PIL import Image
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

class WitchySpider(FromArchiveSpider):
    name = 'witchy'
    allowed_domains = ['witchycomic.com']
    start_urls = ['https://www.witchycomic.com/comic/archive']
    links_regex = [r'comic\/page-\d+'] # nimmt nur die regulären Comics
    rules = (
        Rule(LxmlLinkExtractor(allow=links_regex), callback='parse_item', follow=False),
        )
        
    def _create_page_item(self, response): 
        item = ComicPageHtmlItem()
        item['name'] = self.name
        if re.search(r'page-(\d+)', response.url):
            item['strip_id'] = re.search(r'page-(\d+)', response.url).group(1).zfill(3)
        else:
            item['strip_id'] = 0
        # item['debug'] = response.xpath('//img[@id="cc-comic"]')
        item['title'] = response.xpath('//img[@id="cc-comic"]/@title').get().replace(' ', '-') # gibt's offenbar nicht, deshalb wird der sehr generische Titel genommen
        item['url'] = response.url
        item['img_url'] = response.xpath('//img[@id="cc-comic"]/@src').get()
        item['comment'] = response.xpath('//div[@class="cc-newsbody"]').get()
        item['publ_date'] = response.xpath('//div[@class="cc-publishtime"]/text()').get()
        return item



