# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LackadaisyItem(scrapy.Item):
    # define the fields for your item here like:
    strip_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    comment = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    img_ext = scrapy.Field()
    date = scrapy.Field() # für andere Comics
    name = scrapy.Field() # Für Namen des Comics - wenn ich das Ganze abstrahiere

