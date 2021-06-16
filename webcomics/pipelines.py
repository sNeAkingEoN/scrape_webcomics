# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from . import items
import scrapy
import pandas as pd
import os.path
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path

class MetadataPipeline:
    ''' geht jetzt erstmal davon aus, dass alle Spiders nacheinander abgehandelt werden. 
    Ggf. bei Abstraktion noch mal ein bisschen anders aufziehen...'''

    def open_spider(self, spider):
        self.df = pd.DataFrame()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        csv_row = dict() # Könnte man jetzt auch one-liner draus machen, aber das liest sich nicht unbedingt besser...
        for field in spider.metadata_fields:
            if adapter[field]:
                csv_row[field] = adapter[field]
        self.df = self.df.append(pd.Series(csv_row), ignore_index=True)
        # print('########### Was sagt der Data Frame?')
        # print(self.df)
        return item

    def close_spider(self, spider):
        if self.df.empty:
            return
        sorted_df = self.df.sort_values(by='strip_id').reindex(spider.metadata_fields, axis=1)
        outstring = sorted_df.to_csv(index=False)
        metadata_base_dir = os.path.join(spider.settings['DATA_BASE_DIRECTORY'], 'Data', 'meta')
        outfilename = os.path.join(metadata_base_dir, spider.name + '_meta.csv')
        # Übergeordneter Ordner wird nicht automatisch erstellt:
        if not os.path.exists(metadata_base_dir):
            Path.mkdir(Path(metadata_base_dir))
        with open(outfilename, 'w') as outfile:
            outfile.write(outstring)




            
        





        
