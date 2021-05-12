# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class WebcomicsPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # return super().get_media_requests(item, info)
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    # def file_path(self, request, response=None, info=None):
    #     item = request.meta['item']
    #     print('***********************Item für Filename:')
    #     print(item)
    #     return 'filename'

    # def item_completed(self, results, item, info):
    #     return super().item_completed(results, item, info)



        
