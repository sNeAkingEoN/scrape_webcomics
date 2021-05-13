import re
import scrapy
import os.path
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from ..items import LackadaisyItem


class LackadaisySpider(CrawlSpider):
    name = 'lackadaisy'
    allowed_domains = ['lackadaisycats.com']
    # An Settings aus Projekt rankommen: https://stackoverflow.com/questions/45230147/reading-settings-in-spider-scrapy (30.04.2021)
    settings = get_project_settings()
    base_path = settings.get('WEBCOMICS_BASE_PATH')

    # imgs_path = os.path.join(base_path, 'data', 'imgs', 'lackadaisy')
    # custom_settings = {
    #     "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
    #     "IMAGES_STORE": imgs_path
    # }

    start_urls = ['https://www.lackadaisycats.com/archive.php']

    rules = (
        Rule(LxmlLinkExtractor(allow=r'comic\.php\?comicid=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        strip = LackadaisyItem()
        strip['title'] = response.xpath('//img/@alt').get() # .replace('Lackadaisy ', '') # Falls "Lackadaisy" nicht Teil des Titles ist
        strip['url'] = response.url # != URL zu Datei!
        strip['strip_id'] = re.search(r'(?<=comicid=)\d*', strip['url']).group(0) # https://docs.python.org/3/library/re.html
        strip['image_urls'] = [ response.xpath('//img/@src').get() ]
        strip['comment'] = response.xpath('//div[@class="description"]').get()
        strip['img_ext'] = response.xpath('//img/@src').get().split('.')[-1]
        strip['name'] = self.__class__.name #??
        return strip # was hier returned wird, kommt bei Scraper-Log wieder raus...
