## Tyres web scraping technical assignment

The repository contains python implementations of Scrapy spiders that scrap data regarding offered tyres from the following websites:
* <dexel.co.uk>
* <national.co.uk>

Subsequently, all the retrieved items are exported to a CSV file and saved into the MongoDB collection if specified. 

The repository also includes python scripts for setting up a MongoDB instance using Docker, creating MongoDB database, collection and compound index, running chosen spiders with specified input arguments such as width, profile or rim.

#### Python packages:
Install all packages included in requirements.txt

1. Create a virtual environment (conda, virtualenv etc.).
   - `conda create -n <env_name> python=3.7`
2. Activate your environment.
   - `conda activate <env_name>`
3. Install requirements.
   - `pip install -r requirements.txt `
4. Restart your environment.
    - `conda deactivate`
    - `conda activate <env_name>`

#### Webdriver

Downlaod and set up the Firefox webdriver (other webdriver like Chrome can also be used)

1. Download the Firefox driver ([link](https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-win64.zip) for Windows)

2. Add the localization of the driver to the PATH (Windows):
    - `set PATH=%PATH%;C:\Users\user\Downloads\geckodriver-v0.30.0-win64`

### Docker

1. Install Docker for your system - <https://docs.docker.com/get-docker/>
2. Go to the directory of docker-compose.yaml file and run the following command:
- `docker-compose up -d`

### MongoDB

1. You can check the status of docker containers using:
    - `docker ps`

2. While mongo and mongo-express containers are running, the MongoDB WebUI is available under the ofllowing address:
    - `localhost:8081`

3. Connection to the MongoDB instance can now be established using the URI: 
    - `mongodb://localhost:27017/`

4. Create the database and the collection in MongoDB using python script:
    - `python create_database.py`

MongoDB collections have dynamic schemas, thus we can insert documents containing different fields.

The items returned by the Scrapy pipeline have the following schema:

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
| noise / noise_reduction | str/boolean  |
| winter  | boolean  |
| all_season  | boolean  |
| run_flat | boolean  |
| extra_laod  | boolean  |

Example document:

```
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
```

When loading new items into the database we will perform upsert (update/insert). The match on the manufacturer, tyre_pattern and tyre_size fields will decide whether we have encountered duplicates and we have to update the data or insert new documents into the database.

To increase the performance of most common queries like searching by tyre size (width, profile, rim) and price the compound index was created on the following fields:

| Field name  | Order |
| ------------- | ------------- |
| width  | ASC  |
| profile  | ASC  |
| rim  | ASC  |
| price  | ASC  |

### Running spiders

Use the run_spider.py script and provide the required arguments:
`python run_spider.py --spider dexel --width 175 --profile 50 --rim 15 --dbname tyres --collname tyres` 
`python run_spider.py --spider national --width 205 --profile 55 --rim 16 --dbname tyres --collname tyres`

You could also use the `scrapy crawl <spider_name> -a <k>=<v>` command

### Query the MongoDB database

1. Access the bash of the MongoDB container:
    - `docker exec -it <container_id> bash`  

2. Subsequently, run the `mongo` command to login into the MongoDB (password: "example"):
    - `mongo -u root -p`

3. Change the database:
    - `use tyres`

4. Query the database:

    Search using tyre size:
    `db.tyres.find({width: "205", profile: "55"})` 
    
    Query using tyre size and price condition (less than £70):
    `db.tyres.find({width: "205", profile: "55", rim: "16", price: {"$lt": 90}})`
    
    Search for all season tyres with specified size (205/55/16) and price range (£60 to £80):
    `db.tyres.find({ $and: [ {price: {$lt: 80}}, {price: {$gt: 60}}, {width: "205"}, {profile: "55"}, {rim: "16"}, {all_season: true} ]})`

