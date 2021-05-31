import os.path
import re
import scrapy
from ..items import ComicPageHtmlItem, ComicCanvasImageItem
from pathlib import Path
from PIL import Image
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class FromArchiveSpider(CrawlSpider):
    name = 'archive'
    allowed_domains = []
    start_urls = []
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date','last_modified','comment']
    links_regex = []
    xpaths = []
    max_strip_digits = 4
    rules = (
        Rule(LxmlLinkExtractor(allow=links_regex, restrict_xpaths=xpaths), callback='parse_item', follow=False),
        )
            
    def parse_item(self, response):
        page_item = self._create_page_item(response)
        image_item = self._create_image_item(page_item)
        img_request = scrapy.Request(url=page_item['img_url'], callback=self.save_image, cb_kwargs={'image_item': image_item, 'page_item': page_item})
        yield img_request

    def _create_page_item(self, response): 
        ''' Hier besteht noch Potenzial, weiter zu refactoren'''
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = '' # re.search(r'page-(\d+)', response.url).group(1).zfill(self.max_strip_digits)
        item['title'] = '' # response.xpath('//img[@id="cc-comic"]/@title').get().replace(' ', '-') # gibt's offenbar nicht, deshalb wird der sehr generische Titel genommen
        item['url'] = '' # response.url
        item['img_url'] = '' # response.xpath('//img[@id="cc-comic"]/@src').get()
        item['comment'] = '' # response.xpath('//div[@class="cc-newsbody"]').get()
        item['publ_date'] = '' # response.xpath('//div[@class="cc-publishtime"]/text()').get()
        return item

    def _create_image_item(self, page_item):
        image_item = ComicCanvasImageItem()
        image_item['name'] = page_item['name']
        image_item['url'] = page_item['img_url']
        image_item['id'] = page_item['strip_id']
        image_item['title'] = page_item['title']
        image_item['img_ext'] = image_item['url'].split('.')[-1]
        return image_item

    def save_image(self, response, image_item, page_item):
        image_item['last_modified'] = response.headers['last-modified'].decode('utf-8')
        image_item['img_data'] = response.body
        page_item['last_modified'] = image_item['last_modified'] # Kommt leider nicht mehr in DF an :(

        img_dir = os.path.join(self.settings.get('IMG_BASE_DIRECTORY'), self.name)
        img_file = os.path.join(img_dir,'{}_{}.{}'.format(self.name, image_item['id'], image_item['img_ext']))

        if not os.path.exists(img_dir):
            Path.mkdir(Path(img_dir))

        with open(img_file, 'wb') as imgfile:
            imgfile.write(image_item['img_data'])

        return page_item


