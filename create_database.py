import pymongo

# Connect to the MongoDB instance on the port 27017
myclient = pymongo.MongoClient("mongodb://localhost:27017/",
                                username='root',
                                password='example',)

dblist = myclient.list_database_names()
if "tyres" not in dblist:
    # Create the database if doesn't exist   
    mydb = myclient["tyres"]

collist = mydb.list_collection_names()
if "tyres" in collist:
    # Create the collection if it doesn't exist
    mycol = mydb["tyres"]

