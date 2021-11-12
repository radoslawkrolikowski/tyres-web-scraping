import pymongo
from mongodb_config import mongodb_uri, username, password

# Connect to the MongoDB instance
myclient = pymongo.MongoClient(mongodb_uri,
                               username=username,
                               password=password)

# Create the database and the collection
mydb = myclient["tyres"]
mycol = mydb["tyres"]

# Create the compound index
mycol.create_index([("width" , 1),
                    ("profile", 1),
                    ("rim", 1),
                    ("price", 1)],
                     name="tyre_size_price_idx")

# List the indexes:
print('Available indexes:')
for index in mycol.list_indexes():
    print(index)
