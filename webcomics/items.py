# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComicPageItem(scrapy.Item):
    name = scrapy.Field() # Name of comic / name of spider
    strip_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    comment = scrapy.Field()
    img_ext = scrapy.Field()
    publ_date = scrapy.Field() # Official publication date. Might replace strip id if not present
    last_modified = scrapy.Field() # From HTTP response header: last-modified
    img_data = scrapy.Field()