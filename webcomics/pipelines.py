# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pandas as pd
import os.path
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

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
            outstring += adapter['strip_id'] + '_'
        if adapter.get('title'):
            outstring += adapter['title']
        elif adapter.get('date'):
            outstring += adapter['date']
        else:
            outstring += 'nd'
        outstring += '.'
        if adapter.get('img_ext'):
            outstring += adapter['img_ext']
        else:
            outstring += 'jpg'
        return outstring

class MetadataPipeline:
    ''' geht jetzt erstmal davon aus, dass alle Spiders nacheinander abgehandelt werden. 
    Ggf. bei Abstraktion noch mal ein bisschen anders aufziehen...'''

    data_base_dir = get_project_settings().get('DATA_BASE_DIRECTORY')
    metadata_base_dir = os.path.join(data_base_dir, 'Data', 'meta')

    # Alle Tabellendaten in Dataframe oder so speichern und am Ende sortieren...

    def open_spider(self, spider):
        self.df = pd.DataFrame()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        csv_row = dict() # Könnte man jetzt auch one-liner draus machen, aber das liest sich nicht unbedingt besser...
        for field in spider.metadata_fields:
            if adapter[field]:
                csv_row[field] = adapter[field]
        self.df = self.df.append(pd.Series(csv_row), ignore_index=True)
        return item

    def close_spider(self, spider):
        sorted_df = self.df.sort_values(by='strip_id')
        outstring = sorted_df.to_csv(index=False)
        outfilename = os.path.join(self.__class__.metadata_base_dir, spider.name + '_meta.csv')
        if not os.path.exists(self.__class__.metadata_base_dir):
            Path.mkdir(Path(self.__class__.metadata_base_dir))
        with open(outfilename, 'w') as outfile:
            outfile.write(outstring)




            
        





        
