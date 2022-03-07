import os.path
import re
from urllib.parse import urljoin

import scrapy

from ..items import ComicPageItem
from ..settings import JOBDIR as JD
from .base_spiders import FromStartSpider


class ARedTailsDreamSpider(FromStartSpider):
    name = 'artd'
    allowed_domains = ['minnasundberg.fi']
    start_urls = ['http://minnasundberg.fi/artd.php']
    metadata_fields = ['strip_id', 'url', 'img_url', 'comment', 'publ_date', 'last_modified']
    domain = 'http://minnasundberg.fi'

    max_strip_digits = 3

    custom_settings = {
        "JOBDIR": os.path.join(JD, name)
    }

    def _create_page_item(self, response):
        item = ComicPageItem()
        item['name'] = self.name
        item['strip_id'] = response.xpath('//p[@class="num"]/text()').get().zfill(self.max_strip_digits)
        item['title'] = response.xpath('//meta[@property="og:description"]/@content').get()
        item['url'] = response.url
        item['img_url'] = urljoin(self.domain, 'comic/{}'.format(response.xpath('//div[@id="page"]/img/@src').get()))
        item['comment'] = response.xpath('//div[@id="textbox"]').get()
        item['publ_date'] = ''.join(response.xpath('//div[@id="textbox"]/h1//text()').getall()[1:])
        item['img_ext'] = item['img_url'].split('.')[-1]
        return item

    def _find_first(self, response):
        # return urljoin(self.domain, response.xpath('//area[@id="area2"]/@href').get())
        return 'http://www.minnasundberg.fi/comic/page00.php'

    def _find_next(self,response):
        return urljoin(self.domain, 'comic/{}'.format(response.xpath('//img[contains(@src,"anext.jpg")]/parent::a/@href').get()))

        
