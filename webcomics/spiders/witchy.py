import os.path
import re
import scrapy
from ..items import ComicPageHtmlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings

class WitchySpider(Spider):
    name = 'witchy'
    allowed_domains = ['witchycomic.com']
    metadata_fields = ['strip_id', 'title', 'url', 'publ_date', 'comment']

    def start_requests(self):
        urls = ['https://www.witchycomic.com/comic/page-1']

        # return super().start_requests()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)
            
    def parse_page(self, response):
        # gucken, ob es sich um Seite oder um Bild handelt
        # if response.url.split('.')[:-1] == 'jpg' or 'comics' in response.url.split('/'):
        #     pass
        #     # Treat as image
        #     self.
        # -> Nee, das dürfte nicht passieren.

        metadata_item = self._create_page_item(response=response)
        next_url = response.xpath('//a[@class="cc-next"]/@href').get() # Funktioniert, weil `get()` immer nur das erste Ergebnis liefert!
        # metadata_item['debug'] = next_url

        # yield scrapy.Request(url=metadata_item['img_url'], callback=self.save_image)

        return metadata_item # Todo: Wirft Warnung! - Und Item kommt auch nicht zurück...
        
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

    def _find_next_page(self, response):
        pass
        # das ggf. nicht in extra-Funktion speichern. Kann ich dann aber gucken

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

    def save_image(self, response):
        pass 
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


