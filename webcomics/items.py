# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComicPageHtmlItem(scrapy.Item):
    name = scrapy.Field() # Für Namen des Comics
    strip_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field() # Für Metadaten
    # image_urls = scrapy.Field() - sowas in der Art könnte man nehmen, wenn >1 Bild pro Seite, das könnte aber auch einfach als jeweils neue Seite aufgefasst werden...? Wird wohl erstmal nicht unbedingt passieren...
    comment = scrapy.Field()
    # img_ext = scrapy.Field()
    # download_date = scrapy.Field() # Für Datum des Downloads des Images, aus Response ?
    publ_date = scrapy.Field() # Für Datum, an dem Comic offiziell erschienen ist (bei einigen statt ID)
    last_modified = scrapy.Field() # 
    debug = scrapy.Field()

class ComicCanvasImageItem(scrapy.Item): 
    pass
    name = scrapy.Field() # Für Namen des Comics
    url = scrapy.Field() # URL, unter der das Bild zu finden ist
    id = scrapy.Field() # Comic-Id, wie sie von Website vorgegeben ist
    title = scrapy.Field()
    img_data = scrapy.Field()
    last_modified = scrapy.Field() # zum Nachvollziehen der Daten
    img_ext = scrapy.Field() # mal gucken