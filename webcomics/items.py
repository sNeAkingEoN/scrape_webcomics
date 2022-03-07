# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComicPageItem(scrapy.Item):
    name = scrapy.Field() # Für Namen des Comics bzw. der Spider
    strip_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    comment = scrapy.Field()
    img_ext = scrapy.Field()
    publ_date = scrapy.Field() # Für Datum, an dem Comic offiziell erschienen ist (bei einigen statt ID)
    last_modified = scrapy.Field() # Aus Headern der Response zum Bilderdownload
    img_data = scrapy.Field()