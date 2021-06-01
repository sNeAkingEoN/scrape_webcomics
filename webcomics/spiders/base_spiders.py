import os.path
import re
import scrapy
from ..items import ComicPageHtmlItem
from pathlib import Path
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class FromArchiveSpider(CrawlSpider):
    name = 'archive'
    allowed_domains = []
    start_urls = []
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date','last_modified','comment']
    links_regex = []
    xpaths = []
    rules = (
        Rule(LxmlLinkExtractor(allow=links_regex, restrict_xpaths=xpaths), callback='parse_item', follow=False),
        )

    max_strip_digits = 4
            
    def parse_item(self, response):
        page_item = self._create_page_item(response)
        img_request = scrapy.Request(url=page_item['img_url'], callback=self.save_image, cb_kwargs={'page_item': page_item})
        yield img_request

    def _create_page_item(self, response): 
        ''' Hier besteht noch Potenzial, weiter zu refactoren'''
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = '' 
        item['title'] = ''
        item['url'] = ''
        item['img_url'] = '' 
        item['comment'] = '' 
        item['publ_date'] = '' 
        item['img_ext'] = ''
        return item

    def save_image(self, response, page_item):
        page_item['last_modified'] = response.headers['last-modified'].decode('utf-8')
        page_item['img_data'] = response.body
        page_item['img_ext'] = response.url.split('.')[-1]

        img_dir = os.path.join(self.settings.get('IMG_BASE_DIRECTORY'), self.name)
        img_file = os.path.join(img_dir,'{}_{}.{}'.format(self.name, page_item['strip_id'], page_item['img_ext']))

        if not os.path.exists(img_dir):
            Path.mkdir(Path(img_dir))

        with open(img_file, 'wb') as imgfile:
            imgfile.write(page_item['img_data'])

        return page_item


