import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from time import sleep
from datetime import datetime

class DexelspiderSpider(scrapy.Spider):
    name = 'dexelSpider'
    allowed_domains = ['dexel.co.uk']
    start_urls = ['http://dexel.co.uk/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tyres.pipelines.TyresToCsvPipeline': 100
        }
    }

    def __init__(self, width, profile, rim, filepath):

        super(DexelspiderSpider, self).__init__()

        self.width = width
        self.profile = profile
        self.rim = rim
        self.filepath = filepath

    def parse(self, response):
        query_url = self.start_urls[0] + 'shopping/tyre-results?width=' + str(self.width) \
            + '&profile=' + str(self.profile) + '&rim=' + str(self.rim) + '&speed=.'

        self.driver = webdriver.Firefox()
        self.driver.get(query_url)
        sleep(0.5)

        sel = Selector(text=self.driver.page_source)

        results = sel.xpath('//div[@class="result"]')

        # Create the timestamp object to track when items were scraped
        timestamp = datetime.now()
        
        for result in results:
            sleep(1)
            description = result.xpath('.//*[@class="name"]/text()').extract_first()

            if not description:
                continue 
            
            # Split the description on a new line character. Assume that tyre size is specified in the first line,
            # while second line contains manufacturer and tyre pattern information
            description = description.split('\n')

            tyre_size = description[0]

            if len(description) > 1:
                if len(description[1].strip().split(" ", 1)) > 1:
                    manufacturer = description[1].strip().split(" ", 1)[0]
                    tyre_pattern = description[1].strip().split(" ", 1)[1]
                else:
                    manufacturer = description[1]
                    tyre_pattern = None
            else:
                # Another way the get the manufacturer if description does not contain it
                manufacturer = result.xpath('.//*[@class="manufacturer"]/@alt').extract_first() 
                tyre_pattern = None

            price = result.xpath('.//*[@class="price"]/strong/text()').extract_first().strip('£')
            fuel = result.xpath('.//*[@class="fuel"]/text()').extract_first()
            wetgrip = result.xpath('.//*[@class="wetgrip"]/text()').extract_first()
            noise = result.xpath('.//*[@class="noise"]/text()').extract_first().strip(' dB')

            winter = result.xpath('.//li[not(contains(@style, "display:none")) and @class="wn"]/img/@alt').extract_first() 
            all_season = result.xpath('.//li[not(contains(@style, "display:none")) and @class="al"]/img/@alt').extract_first() 
            run_flat = result.xpath('.//li[not(contains(@style, "display:none")) and @class="rf"]/img/@alt').extract_first() 
            extra_load = result.xpath('.//li[not(contains(@style, "display:none")) and @class="el"]/img/@alt').extract_first() 

            yield {
                'manufacturer': manufacturer,
                'tyre_size': tyre_size,
                'tyre_pattern': tyre_pattern,
                'price': price,
                'fuel': fuel,
                'wetgrip': wetgrip,
                'noise': noise,
                'winter': True if winter else False,
                'all_season': True if all_season else False,
                'run_flat': True if run_flat else False,
                'extra_laod': True if extra_load else False,
                'timestamp': timestamp
            }
