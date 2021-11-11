import pymongo
from mongodb_config import mongodb_uri, username, password

# Connect to the MongoDB instance
myclient = pymongo.MongoClient(mongodb_uri,
                               username=username,
                               password=password)

dblist = myclient.list_database_names()
if "tyres" not in dblist:
    # Create the database if doesn't exist   
    mydb = myclient["tyres"]

collist = mydb.list_collection_names()
if "tyres" in collist:
    # Create the collection if it doesn't exist
    mycol = mydb["tyres"]

