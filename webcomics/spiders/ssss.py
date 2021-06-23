import os.path
import re
import scrapy
from .base_spiders import FromArchiveSpider
from ..items import ComicPageHtmlItem
from pathlib import Path
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

class StandStillStaySilenSpider(FromArchiveSpider):
    name = 'ssss'
    allowed_domains = ['sssscomic.com']
    start_urls = ['https://sssscomic.com/?id=archive']
    links_regex = [r'comic2\.php\?page=\d+', r'comic\.php\?page=\d+'] # nimmt nur die Comics aus dem 2. Adventure, for brevity.
    rules = (
        Rule(LxmlLinkExtractor(allow=links_regex), callback='parse_item', follow=False),
        )
    max_strip_digits = 3
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date','last_modified','comment']

    custom_settings = {
        "JOBDIR": os.path.join(JD, name)
    }

    def _create_page_item(self, response): 
        item = ComicPageHtmlItem()
        item['name'] = self.name
        if not 'comic2' in response.url:
            item['strip_id'] = '1-{}'.format(response.url.split('=')[-1].zfill(self.max_strip_digits))
        else:
            item['strip_id'] = '2-{}'.format(response.url.split('=')[-1].zfill(self.max_strip_digits)) 
        item['title'] = response.xpath('//title/text()').get().replace(' ', '-') # gibt's offenbar nicht, deshalb wird der sehr generische Titel genommen
        item['url'] = response.url
        item['img_url'] = "https://{}/{}".format(self.allowed_domains[0], response.xpath('//img[@class="comicnormal"]/@src').get().strip())
        item['comment'] = response.xpath('//div[@id="comic_text"]/span[@id="comicdate"]/following-sibling::p').get() # ist noch komplexer, kann z.B. noch img enthalten. Aber einfach `following-sibling::*` geht auch nicht, weil ich dann die ganze Comments-Section mit abgreife
        item['publ_date'] = response.xpath('//div[@id="comic_text"]/span[@id="comicdate"]/text()').get()
        return item



