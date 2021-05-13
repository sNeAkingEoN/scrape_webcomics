# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class WebcomicImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta.get('item')
        return self.create_img_file_name(item)
        
    def create_img_file_name(self, item):
        adapter = ItemAdapter(item)
        outstring = ''   
        if adapter.get('name'):
            outstring += '{0}/{0}_'.format(adapter['name'])
        if adapter.get('strip_id'):
            outstring += adapter['strip_id'].zfill(5) + '_'
        if adapter.get('title'):
            outstring += adapter['title']
        elif adapter.get('date'):
            outstring += adapter['date']
        else:
            outstring += 'nd'
        outstring += '.'
        if 'img_ext' in adapter.keys():
            outstring += adapter['img_ext']
        else:
            outstring += 'jpg'
        return outstring

    # def item_completed(self, results, item, info):
    #     return super().item_completed(results, item, info)



        
