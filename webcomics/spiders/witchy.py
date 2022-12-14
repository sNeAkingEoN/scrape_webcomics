import os.path
import re
from pathlib import Path

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

from ..items import ComicPageItem
from ..settings import JOBDIR as JD
from .base_spiders import FromArchiveSpider


class WitchySpider(FromArchiveSpider):
    name = 'witchy'
    allowed_domains = ['witchycomic.com']
    start_urls = ['https://www.witchycomic.com/comic/archive']
    links_regex = [r'comic\/page-\d+'] # Only regular comics, no guest art
    rules = (
        Rule(LxmlLinkExtractor(allow=links_regex), callback='parse_item', follow=False),
        )
    max_strip_digits = 3
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date','last_modified','comment']

    custom_settings = {
        "JOBDIR": os.path.join(JD, name)
    }

    def _create_page_item(self, response): 
        item = ComicPageItem()
        item['name'] = self.name
        if re.search(r'page-(\d+)', response.url):
            item['strip_id'] = re.search(r'page-(\d+)', response.url).group(1).zfill(self.max_strip_digits)
        else:
            item['strip_id'] = '0'
        item['title'] = response.xpath('//img[@id="cc-comic"]/@title').get().replace(' ', '-') # Only a generic title here
        item['url'] = response.url
        item['img_url'] = response.xpath('//img[@id="cc-comic"]/@src').get()
        item['comment'] = response.xpath('//div[@class="cc-newsbody"]').get()
        item['publ_date'] = response.xpath('//div[@class="cc-publishtime"]/text()').get()
        return item



