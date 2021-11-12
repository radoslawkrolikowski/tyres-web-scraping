Create the virtual environment:

conda create -n tyres-web-scraping python==3.7 

OR

python3 -m venv /home/debian/Documents/web-scraping

Activate the environment:

conda activate tyres-web-scraping 

OR

source /home/debian/Documents/web-scraping/bin/activate


pip install Scrapy
pip install selenium
pip install pymongo

Download the Firefox driver:

https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-win64.zip


Add the localization of the driver to the PATH:

`set PATH=%PATH%;C:\Users\user\Downloads\geckodriver-v0.30.0-win64`


Go to the directory of docker-compose.yaml file and run the following command:

`docker-compose up -d`

MongoDb WebUI is available under the ollowing address:

localhost:8081

Connection to the MongoSb instance can now be established using the URI: 

mongodb://localhost:27017/

Create the database and the collection in MongoDB:

Run the following command:

`python create_database.py`

MongoDB collections have dynamic schemas, thus we can insert documents containing different fields.

The items inserted into the database by Scrapy pipeline will impose the following schema:

| Field name  | Type |
| ------------- | ------------- |
| manufacturer  | str  |
| width  | str  |
| profile  | str  |
| rim  | str  |
| tyre_pattern  | str  |
| price | float  |
| fuel | str  |
| wetgrip  | str  |
| noise / noise_reduction | str  |
| winter  | boolean  |
| all_season  | boolean  |
| run_flat | boolean  |
| extra_laod  | boolean  |

Example document:

{
    _id: ObjectId('618e5db5d5143165a3453060'),
    manufacturer: 'Hankook',
    tyre_pattern: 'Ventus Prime 3 (K125)',
    tyre_size: '205/55 R16 91W Hankook Ventus Prime 3 (K125)',
    all_season: false,
    extra_laod: false,
    fuel: 'F',
    noise: '69',
    price: 87.84,
    profile: '55',
    rim: '16',
    run_flat: true,
    website: 'http://dexel.co.uk/',
    wetgrip: 'C',
    width: '205',
    winter: false
}

When loading new items into the database we will perform upsert (update/insert). The match on the manufacturer, tyre_pattern and tyre_size fields will decide whether we have encountered duplicates and we have to update the data or insert new documents into the database.


To increase the performance of most common queries like searching by tyre size (width, profile, rim) and price the compound index was created on the following fields:

| Field name  | Order |
| ------------- | ------------- |
| width  | ASC  |
| profile  | ASC  |
| rim  | ASC  |
| price  | ASC  |


Run the spider with:
`python run_spider.py --spider dexel --width 175 --profile 50 --rim 15 --dbname tyres --collname tyres` 

`python run_spider.py --spider national --width 205 --profile 55 --rim 16 --dbname tyres --collname tyres`

Query the database

Access the bash of the MongoDB container:

`docker exec -it <container_id> bash`  

Subsequently run the mongo command to login into the MongoDB (password: "example"):

`mongo -u root -p`

Change the DB:

`use tyres`

Search using tyre size:

db.tyres.find({width: "205", profile: "55"}) 

Query using tyre size and price condition (less than £70):

db.tyres.find({width: "205", profile: "55", rim: "16", price: {"$lt": 90}})

Search for all season tyres with specified size (205/55/16) and price range (£60 to £80):

db.tyres.find({ $and: [ {price: {$lt: 80}}, {price: {$gt: 60}}, {width: "205"}, {profile: "55"}, {rim: "16"}, {all_season: true} ]})  

