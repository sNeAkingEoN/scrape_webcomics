import os.path
import re
from pathlib import Path

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

from ..items import ComicPageItem
from ..settings import JOBDIR as JD
from .base_spiders import FromArchiveSpider


class StandStillStaySilentSpider(FromArchiveSpider):
    name = 'ssss'
    allowed_domains = ['sssscomic.com']
    start_urls = ['https://sssscomic.com/?id=archive']
    links_regex = [r'comic2\.php\?page=\d+', r'comic\.php\?page=\d+']
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
        if not 'comic2' in response.url:
            item['strip_id'] = '1-{}'.format(response.url.split('=')[-1].zfill(self.max_strip_digits))
        else:
            item['strip_id'] = '2-{}'.format(response.url.split('=')[-1].zfill(self.max_strip_digits)) 
        item['title'] = response.xpath('//title/text()').get().replace(' ', '-') # Only generic titles for comic pages
        item['url'] = response.url
        item['img_url'] = "https://{}/{}".format(self.allowed_domains[0], response.xpath('//img[@class="comicnormal"]/@src').get().strip())
        item['comment'] = response.xpath('//div[@id="comic_text"]/span[@id="comicdate"]/following-sibling::p').get() # quite complex part to scrape. `following-sibling::*` would get the whole comment section, which is not desired.
        item['publ_date'] = response.xpath('//div[@id="comic_text"]/span[@id="comicdate"]/text()').get()
        return item



