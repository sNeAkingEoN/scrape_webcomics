import os.path
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from ..items import ComicPageHtmlItem
from ..settings import JOBDIR as JD


class LackadaisySpider(CrawlSpider):
    name = 'lackadaisy'
    allowed_domains = ['lackadaisycats.com']
    # An Settings aus Projekt rankommen: https://stackoverflow.com/questions/45230147/reading-settings-in-spider-scrapy (30.04.2021)
    # - das braucht die Spider eigentlich nicht, nur die Pipeline o.ä.
    metadata_fields = ['strip_id', 'title', 'url', 'comment', 'download_date']

    # Might need in the future:
    # imgs_path = os.path.join(base_path, 'data', 'imgs', 'lackadaisy')
    # custom_settings = {
    #     "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
    #     "IMAGES_STORE": imgs_path
    # }

    start_urls = ['https://www.lackadaisycats.com/archive.php']

    rules = (
        Rule(LxmlLinkExtractor(allow=r'comic\.php\?comicid=\d+'), callback='parse_item', follow=False),
    )

    custom_settings = {
        "JOBDIR": os.path.join(JD, name)
    }

    def parse_item(self, response):
        strip = ComicPageHtmlItem()
        strip['name'] = self.__class__.name
        strip['title'] = response.xpath('//img/@alt').get() # .replace('Lackadaisy ', '') # Falls "Lackadaisy" nicht Teil des Titles ist
        strip['url'] = response.url # != URL zu Datei!
        strip['strip_id'] = re.search(r'(?<=comicid=)\d*', strip['url']).group(0).zfill(3) # https://docs.python.org/3/library/re.html
        strip['image_urls'] = [ response.xpath('//img/@src').get() ]
        strip['comment'] = response.xpath('//div[@class="description"]').get()
        strip['img_ext'] = response.xpath('//img/@src').get().split('.')[-1]
        strip['download_date'] = 'placeholder'
        return strip # was hier returned wird, kommt bei Scraper-Log wieder raus...
