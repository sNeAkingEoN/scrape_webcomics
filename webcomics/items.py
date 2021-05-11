# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LackadaisyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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

    def save_item(self, save_to_file):
        '''deprecated '''
        print(self['title'])
        csv_line = self['strip_id'] + ',' + self['title'] + ',' + self['img_url'] + '\n'
        # es fehlt noch: comment. Muss man aufpassen wegen dem Separator. Aber vllt. brauche ich dafür ohnehin eine extra-library?
        # Wahrscheinlich fehlt noch mehr... aber ist ja erstmal ein Prototyp
        with open(save_to_file, 'a') as infile:
            infile.write(csv_line)


