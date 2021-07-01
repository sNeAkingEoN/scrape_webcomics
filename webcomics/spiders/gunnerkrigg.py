import os.path
import pandas as pd
import scrapy
from ..items import ComicPageHtmlItem
from .base_spiders import FromStartSpider
from ..settings import JOBDIR as JD

class GunnerkriggSpider(FromStartSpider):
    name = 'gunnerkrigg'
    allowed_domains = ['gunnerkrigg.com']
    start_urls = ['https://www.gunnerkrigg.com']
    metadata_fields = ['strip_id', 'url', 'img_url', 'comment', 'publ_date']
    domain = start_urls[0]
    archive_url = os.path.join(domain, 'archives/')
    max_strip_digits = 4

    custom_settings = {
        "JOBDIR": os.path.join(JD, name)
    }

    def parse(self, response):
        archive_request = scrapy.Request(url=self.archive_url, callback=self.parse_archive)
        link_to_first = self._find_first(response)
        return (archive_request, scrapy.Request(url=link_to_first, callback=self.parse_page))

    def _create_page_item(self, response):
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = response.url.split('=')[-1]
        item['title'] = None
        item['url'] = response.url
        item['img_url'] = '{}{}'.format(self.domain, response.xpath('//img[@class="comic_image"]/@src').get())
        item['comment'] = response.xpath('//div[@class="content"]/p').get()
        item['publ_date'] = response.xpath('//div[@class="content"]/a[@class="important"]/following-sibling::text()').get()
        item['img_ext'] = item['img_url'].split('.')[-1]
        return item

    def _find_first(self, response):
        return '{}/{}'.format(self.domain, response.xpath('//img[@src="/images/first_a.jpg"]/parent::a/@href').get())

    def _find_next(self,response):
        return '{}/{}'.format(self.domain, response.xpath('//img[@src="/images/next_a.jpg"]/parent::a/@href').get())

    def parse_archive(self, response):
        chapter_titles = response.xpath('//h4/text()').getall()[1:]
        chapter_starts = [x.split('=')[-1] for x in response.xpath('//a[@class="chapter_button"]/@href').getall()]  
        if not len(chapter_titles) == len(chapter_starts):
            print("Achtung! Kapitel und Seitenzahlen passen nicht zusammen. Kapitel:", len(chapter_titles), "Seitenzahlen:",len(chapter_starts))
        
        chapter_index = pd.DataFrame({"Page": chapter_starts, "Chapter": chapter_titles})

        self.metadata_base_dir = os.path.join(self.settings['DATA_BASE_DIRECTORY'], 'Data', 'meta')
        self.indexdata_file_name = os.path.join(self.metadata_base_dir, self.name + '_index.csv')

        with open(self.indexdata_file_name, 'w') as outfile:
            outfile.write(chapter_index.to_csv(index=False))



            
        

        
