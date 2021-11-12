# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import logging
import pymongo
from mongodb_config import mongodb_uri, username, password


class TyresToCsvPipeline:
    """Implementation of the Scrapy Pipeline that saves scraped items to CSV file.
 
    Parameters
    ----------
    filepath: str
        File path that determines where to save the CSV file (for example, /home/tyres.csv)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = open(self.filepath, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(filepath=crawler.spider.filepath)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        logging.info('Items saved to {}'.format(self.filepath))


class TyresToMongoDbPipeline:
    """Implementation of the Scrapy Pipeline that upserts scraped items to the MongeDB
    collection as specified by db_name and coll_name. To perform authorization you have to firstly import
    the username and password from an external file.

    Pipeline updates/inserts items based on the following selection criteria (fileds):
        {'manufacturer', 'description', 'tyre_pattern'}

    Parameters
    ----------
    db_name: str
        MongoDB database name. If the db_name is None then the pipeline doesn't save items to MongoDB.
    coll_name: str
        MongoDB collection name.
    """
    def __init__(self, db_name, coll_name):
        self.db_name = db_name
        self.coll_name = coll_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_name=crawler.spider.db_name,
                   coll_name=crawler.spider.coll_name)

    def open_spider(self, spider):
        ## Initializing connection to MongoDB
        if self.db_name:
            self.client = pymongo.MongoClient(mongodb_uri, username=username, password=password)
            self.db = self.client[self.db_name]

    def close_spider(self, spider):
        if self.db_name:
            self.client.close()
            logging.info("Items saved to MongoDB")

    def process_item(self, item, spider):
        if self.db_name:
            filter = {'manufacturer': item['manufacturer'],
                      'tyre_size': item['tyre_size'],
                      'tyre_pattern': item['tyre_pattern']}
            # Perform upsert one item at a time
            self.db[self.coll_name].update_one(filter, {"$set": item}, upsert=True)
            return item
        else:
            return item