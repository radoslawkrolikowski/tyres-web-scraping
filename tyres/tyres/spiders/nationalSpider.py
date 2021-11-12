import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from time import sleep


class NationalspiderSpider(scrapy.Spider):
    """Implementation of the Scrapy Spider that extracts tyres information
    from national.co.uk
    ----------
    width: str
        Tyre width.
    profile: str
        Tyre profile.
    rim: str
        Rim size.
    filepath: str
        File path that determines where to save the CSV file (for example, /home/tyres.csv)
    db_name: str
        MongoDB database name. If the db_name is None then the pipeline doesn't save items to MongoDB.
    coll_name: str
        MongoDB collection name.

    Yields
    ------
    dict
        Dictionary that represents scraped item.
    """
    name = 'nationalSpider'
    allowed_domains = ['national.co.uk']
    start_urls = ['http://national.co.uk/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tyres.pipelines.TyresToCsvPipeline': 100,
            'tyres.pipelines.TyresToMongoDbPipeline': 200
        }
    }

    def __init__(self, width, profile, rim, filepath, db_name, coll_name):

        super(NationalspiderSpider, self).__init__()

        self.width = width
        self.profile = profile
        self.rim = rim
        self.filepath = filepath
        self.db_name = db_name
        self.coll_name = coll_name

    def parse(self, response):

        query_url = self.start_urls[0] + 'tyres-search?width=' + str(self.width) \
            + '&profile=' + str(self.profile) + '&diameter=' + str(self.rim)

        self.driver = webdriver.Firefox()
        self.driver.get(query_url)
        sleep(1)

        sel = Selector(text=self.driver.page_source)

        results = sel.xpath('//div[@class="col-md-6 tyreDisplay"]')

        for result in results:
            sleep(1)

            manufacturer = result.xpath('.//@data-brand').extract_first() 
            wetgrip = result.xpath('.//@data-grip').extract_first().split()[-1]

            run_flat = result.xpath('.//@data-brand').extract_first()
            run_flat = False if run_flat == 'No' else True

            winter = result.xpath('.//@data-tyre-season').extract_first()
            winter = True if winter == 'Winter' else False

            all_season = result.xpath('.//@data-tyre-season').extract_first()
            all_season = True if all_season == 'All Season' else False

            price = result.xpath('.//@data-sort').extract_first()
            price = float(price) if price else None

            extra_laod = result.xpath('.//@data-extraload').extract_first()
            extra_laod = False if extra_laod == 'No' else True

            fuel = result.xpath('.//@data-fuel').extract_first().split()[-1]      

            noise_reduction = result.xpath('.//@data-noisereduction').extract_first()
            noise_reduction = False if noise_reduction == 'No' else True

            tyre_pattern = result.xpath('.//*[@class="pattern_link"]/text()').extract_first() 

            tyre_size = result.xpath('.//*[@class="pattern_link"]/parent::p/following-sibling::p[1]/text()').extract_first().strip()

            yield {
                'website': self.start_urls[0],
                'manufacturer': manufacturer,
                'width': self.width,
                'profile': self.profile,
                'rim': self.rim,
                'tyre_pattern': tyre_pattern,
                'tyre_size': tyre_size,
                'price': price,
                'fuel': fuel,
                'wetgrip': wetgrip,
                'noise_reduction': noise_reduction,
                'winter': winter,
                'all_season': all_season,
                'run_flat': run_flat,
                'extra_laod': extra_laod,
            }


