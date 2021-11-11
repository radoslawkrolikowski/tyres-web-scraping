import argparse
from scrapy.crawler import CrawlerProcess
from tyres.spiders.dexelSpider import DexelspiderSpider
from datetime import datetime


# Example input arguments
# width = "175"
# profile = "50"
# rim = "15"
# filepath = "dexel.csv"
# dbname = "tyres"
# collname = "tyres"

# Example command:
# python run_spider.py --spider dexel --width 175 --profile 50 --rim 15 --dbname tyres --collname tyres
 
if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    })

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--spider",
        help="Spider name",
        choices=["dexel"],
        required=True
    )
    parser.add_argument(
        "--width",
        type=str,
        help="Tyre width",
        required=True
    )

    parser.add_argument(
        "--profile",
        type=str,
        help="Profile",
        required=True
    )

    parser.add_argument(
        "--rim",
        type=str,
        help="Rim",
        required=True
    )

    parser.add_argument(
        "--filepath",
        type=str,
        help="Where to save the exported CSV file",
    )

    parser.add_argument(
        "--dbname",
        type=str,
        help="Name of the MongoDB database",
    )

    parser.add_argument(
        "--collname",
        type=str,
        help="Name of the MongoDB collection",
    )

    args = parser.parse_args()

    if args.spider == "dexel":
        if not args.filepath:
            args.filepath = datetime.now().strftime('%Y-%m-%d-%H-%M') + '_' + args.spider + '.csv'

        process.crawl(DexelspiderSpider, width=args.width, profile=args.profile, rim=args.rim, filepath=args.filepath, db_name=args.dbname, coll_name=args.collname)
        process.start() # the script will block here until the crawling is finished
    else:
        pass



