import os.path
import re
import scrapy
from ..items import ComicPageHtmlItem, ComicCanvasImageItem
from pathlib import Path
from PIL import Image
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

class WitchySpider(CrawlSpider):
    name = 'witchy'
    allowed_domains = ['witchycomic.com']
    start_urls = ['https://www.witchycomic.com/comic/archive']
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date','last_modified','comment']
    rules = (
        Rule(LxmlLinkExtractor(allow=[r'comic\/page-\d+']), callback='parse_item', follow=False),
        )
        # , r'comics\/[-\w]+\.jpg' # in allow

        # restrict_xpaths='//a[@class="cc-next"]'

        # return super().start_requests()
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
            
    def parse_item(self, response):
        page_item = self._create_page_item(response)
        # print('<3<3<3<3img_url:', page_item['img_url'])
        image_item = self._create_image_item(page_item)
        img_request = scrapy.Request(url=page_item['img_url'], callback=self.save_image, cb_kwargs={'image_item': image_item, 'page_item': page_item}) # evtl. noch ändern oder erweitern um titel
        yield img_request
        # print('#+#+#+#+#+#+#+# In parse_item')
        # # gucken, ob es sich um Seite oder um Bild handelt
        # if response.url.split('.')[:-1] == 'jpg' or 'comics' in response.url.split('/'):
        #     print('~~~~~~~~~~ Image found! ~~~~~~~~~~~~')
        #     pass
        #     # Treat as image
        # elif 'comic' in response.url.split('/'):
        #     print('+++++++++++++++++ Page found ****************')
        #     page_item = self._create_page_item(response)
        #     return page_item

        # metadata_item = self._create_page_item(response=response)
        # next_url = response.xpath('//a[@class="cc-next"]/@href').get() # Funktioniert, weil `get()` immer nur das erste Ergebnis liefert!
        # # metadata_item['debug'] = next_url

        # # yield scrapy.Request(url=metadata_item['img_url'], callback=self.save_image)

        # return metadata_item # Todo: Wirft Warnung! - Und Item kommt auch nicht zurück...
        
        # Item (Metadaten) erstellen (-> Funktion?) - DONE
        # Wird ggf. für nächsten Schritt gebraucht

        # URL der nächsten Seite rausgeben (-> Funktion) - Done - ist one-liner, deshalb erstmal keine eigene Fkt.

        # Link zu Image finden und Request dafür absetzen (-> Callback-Funktion)

        # Item (Metadaten) returnen - wird dann ganz normal in Pipeline weiterverarbeitet (hoffentlich)

    # ~~~~ Und immer schön yielden! ~~~~ #

        # Falls Seite: nächste Seite suchen und zu Start-Urls hinzufügen
        # Außerdem ComicPageHtmlItem fertig machen und losschicken
        # Entweder den start_urls hinzufügen oder hier Request losschicken...?!?
        # -> nee, wahrscheinlich den Start-Urls hinzufügen UND returnen, für die Pipeline

        # Falls Bild: ComicCanvasImageItem fertig machen und Request losschicken
        # Braucht wahrscheinlich noch Extra-Callbackfunktion zum Speichern und alles 

    def _create_page_item(self, response): 
        item = ComicPageHtmlItem()
        item['name'] = self.name
        item['strip_id'] = re.search(r'page-(\d+)', response.url).group(1).zfill(3)
        # item['debug'] = response.xpath('//img[@id="cc-comic"]')
        item['title'] = response.xpath('//img[@id="cc-comic"]/@title').get().replace(' ', '-') # gibt's offenbar nicht, deshalb wird der sehr generische Titel genommen
        item['url'] = response.url
        item['img_url'] = response.xpath('//img[@id="cc-comic"]/@src').get()
        item['comment'] = response.xpath('//div[@class="cc-newsbody"]').get()
        item['publ_date'] = response.xpath('//div[@class="cc-publishtime"]/text()').get()
        return item

    def _create_image_item(self, page_item):
        image_item = ComicCanvasImageItem()
        image_item['name'] = page_item['name']
        image_item['url'] = page_item['img_url']
        image_item['id'] = page_item['strip_id']
        image_item['title'] = page_item['title']
        image_item['img_ext'] = image_item['url'].split('.')[-1]
        return image_item

    def save_image(self, response, image_item, page_item):
        # print('****************** Inside save_image *************')
        image_item['last_modified'] = response.headers['last-modified'].decode('utf-8')
        image_item['img_data'] = response.body
        page_item['last_modified'] = image_item['last_modified'] # Kommt leider nicht mehr in DF an :(

        img_dir = os.path.join(self.settings.get('IMG_BASE_DIRECTORY'), self.name)
        img_file = os.path.join(img_dir,'{}_{}.{}'.format(self.name, image_item['id'], image_item['img_ext']))

        if not os.path.exists(img_dir):
            Path.mkdir(Path(img_dir))

        with open(img_file, 'wb') as imgfile:
            imgfile.write(image_item['img_data'])

        return page_item
        # print(page_item)

        # hier Bild speichern
        # base_path = self.settings.IMG_BASE_DIRECTORY







        # strip = ComicPageHtmlItem()
        # strip['name'] = self.__class__.name
        # strip['title'] = response.xpath('//img/@alt').get() # .replace('Lackadaisy ', '') # Falls "Lackadaisy" nicht Teil des Titles ist
        # strip['url'] = response.url # != URL zu Datei!
        # strip['strip_id'] = re.search(r'(?<=comicid=)\d*', strip['url']).group(0).zfill(3) # https://docs.python.org/3/library/re.html
        # strip['image_urls'] = [ response.xpath('//img/@src').get() ]
        # strip['comment'] = response.xpath('//div[@class="description"]').get()
        # strip['img_ext'] = response.xpath('//img/@src').get().split('.')[-1]
        # strip['download_date'] = 'placeholder'
        # return strip # was hier returned wird, kommt bei Scraper-Log wieder raus...


