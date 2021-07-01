import os.path
import re
from pathlib import Path
from abc import ABC, abstractmethod

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider

from ..items import ComicPageHtmlItem


class FromArchiveSpider(CrawlSpider, ABC):
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

    @abstractmethod
    def _create_page_item(self, response): 
        pass

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

        page_item['img_data'] = 'removed' # Easier log output
        return page_item


class FromStartSpider(Spider, ABC):
    name = ''
    allowed_domains = []
    start_urls = []
    metadata_fields = ['strip_id', 'title', 'url', 'img_url', 'comment', 'publ_date']
    max_strip_digits = 4

    def parse(self, response):
        link_to_first = self._find_first(response)
        yield scrapy.Request(url=link_to_first, callback=self.parse_page) 

    def parse_page(self, response):
        page_item = self._create_page_item(response)
        link_to_next = self._find_next(response)
        img_request = scrapy.Request(url=page_item['img_url'], callback=self.save_image, cb_kwargs={'page_item': page_item})
        if link_to_next:
            next_request = scrapy.Request(url=link_to_next, callback=self.parse_page)
            return (next_request, img_request)
        else:
            return img_request

    def save_image(self, response, page_item):
        page_item['last_modified'] = response.headers['last-modified'].decode('utf-8')
        page_item['img_data'] = response.body
        page_item['img_ext'] = response.url.split('.')[-1]

        img_dir = os.path.join(self.settings.get('IMG_BASE_DIRECTORY'), self.name)
        img_file = os.path.join(img_dir,'{}_{}.{}'.format(self.name, page_item['strip_id'].zfill(self.max_strip_digits), page_item['img_ext']))

        if not os.path.exists(img_dir):
            Path.mkdir(Path(img_dir))

        with open(img_file, 'wb') as imgfile:
            imgfile.write(page_item['img_data'])

        page_item['img_data'] = 'removed' # Easier log output
        return page_item

    @abstractmethod
    def _create_page_item(self, response):
        pass

    @abstractmethod
    def _find_first(self, response):
        pass

    @abstractmethod
    def _find_next(self,response):
        pass
    
