# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class TyresToCsvPipeline:
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