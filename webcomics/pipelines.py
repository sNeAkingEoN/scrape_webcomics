# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
from pathlib import Path

import pandas as pd
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from . import items


class MetadataPipeline:
    ''' geht jetzt erstmal davon aus, dass alle Spiders nacheinander abgehandelt werden. 
    Ggf. bei Abstraktion noch mal ein bisschen anders aufziehen...'''
    metadata_base_dir = ''
    metadata_file_name = ''
    df = None

    def open_spider(self, spider):
        self.metadata_base_dir = spider.settings['META_BASE_DIRECTORY']
        self.metadata_file_name = os.path.join(self.metadata_base_dir, spider.name + '_meta.csv')
        if os.path.isfile(self.metadata_file_name):
            self.df = pd.read_csv(self.metadata_file_name,dtype="string")
            print("+++++++++++++++++++++Geöffneter DF:")
            print(self.df)
        else:
            self.df = pd.DataFrame()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        csv_row = dict() # Könnte man jetzt auch one-liner draus machen, aber das liest sich nicht unbedingt besser...
        for field in spider.metadata_fields:
            if adapter[field]:
                csv_row[field] = adapter[field]
            # else:
            #     csv_row[field] = 'n.A.'
        self.df = self.df.append(pd.Series(csv_row), ignore_index=True)
        # print('########### Was sagt der Data Frame?')
        # print(self.df)
        return item

    def close_spider(self, spider):
        print("+++++ Was sagt der DataFrame?", self.df)
        if self.df.empty:
            print("****** Oops! Problem mit DataFrame: DF ist empty")
            return
        sorted_df = self.df.sort_values(by='strip_id').reindex(spider.metadata_fields, axis=1).drop_duplicates()
        outstring = sorted_df.to_csv(index=False)
        # Übergeordneter Ordner wird nicht automatisch erstellt:
        if not os.path.isdir(self.metadata_base_dir):
            Path.mkdir(Path(self.metadata_base_dir))
        with open(self.metadata_file_name, 'w') as outfile:
            outfile.write(outstring)




            
        





        
