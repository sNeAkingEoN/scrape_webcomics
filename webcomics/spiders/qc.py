import os.path
import pandas as pd
import re
import scrapy
from ..items import ComicPageHtmlItem
from .base_spiders import FromStartSpider
from bs4 import BeautifulSoup
from ..settings import JOBDIR as JD

class QuestionableContentSpider(FromStartSpider):
    name = 'qc'
    allowed_domains = ['questionablecontent.net']
    start_urls = ['https://www.questionablecontent.net/']
    domain = start_urls[0]
    archive_url = os.path.join(domain, 'archive.php')
    metadata_fields = ['strip_id', 'url', 'img_url', 'comment']

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
        item['strip_id'] = response.url.split('=')[-1].zfill(self.max_strip_digits)
        item['title'] = ''
        item['url'] = response.url
        item['img_url'] = os.path.join(self.domain, os.path.normpath(response.xpath('//img[@id="strip"]/@src').get()))
        item['comment'] = response.xpath('//div[@id="news"]').get()
        item['img_ext'] = item['img_url'].split('.')[-1]
        return item

    def parse_archive(self, response):
        df = pd.DataFrame(columns=['strip_id', 'title', 'is_guest'])
        raw_titles = response.xpath('//center/following::div[@class="small-12 medium-expand column"]/a').getall() 
        # Filter infos
        for title in raw_titles:
            soup = BeautifulSoup(title, 'html.parser')
            url = soup.a['href']
            text = soup.a.get_text()
            parts = text.split(': ')
            pt1 = parts[0]
            pt2 = ': '.join(parts[1:])
            strp_id = re.search(r'\d+', pt1).group(0).zfill(self.max_strip_digits)
            strp_title = pt2.strip()
            is_guest = self._is_guest(pt2)
            df = df.append({'strip_id': strp_id, 'title': strp_title, 'is_guest': is_guest}, ignore_index=True)
        df = df.drop_duplicates().sort_values(by='strip_id')
        self.metadata_base_dir = os.path.join(self.settings['DATA_BASE_DIRECTORY'], 'Data', 'meta')
        self.indexdata_file_name = os.path.join(self.metadata_base_dir, self.name + '_index.csv')

        with open(self.indexdata_file_name, 'w') as outfile:
            outfile.write(df.to_csv(index=False))

    def _find_first(self, response):
        # return '{}/{}'.format(self.domain, response.xpath('//a[text()="First"]/@href').get())
        return os.path.join(self.domain, response.xpath('//a[text()="First"]/@href').get())

    def _find_next(self,response):
        return '{}/{}'.format(self.domain, response.xpath('//a[text()="Next"]/@href').get())
                # return os.path.join(self.domain, response.xpath('//a[text()="First"]/@href').get())

    def _is_guest(self, titlestring):
        for searchstring in 'guest comic', 'guest strip', 'guest week', 'guest-comic', 'guest artiste':
            if searchstring in titlestring.lower():
                return True
        return False

        
