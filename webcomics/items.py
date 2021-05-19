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
    comment = scrapy.Field()
    image_urls = scrapy.Field()
    img_ext = scrapy.Field()
    download_date = scrapy.Field() # Für Datum des Downloads des Images, aus Response
    date = scrapy.Field()

