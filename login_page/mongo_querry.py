import pymongo
from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('rnsit@123')
cluster = pymongo.MongoClient("mongodb+srv://%s:%s@rnsece-5xj7v.mongodb.net/<dbname>?retryWrites=true&w=majority" % (username, password))

#cluster = MongoClient('mongodb://%s:%s@rnsit-ecert.7ufby.mongodb.net/test?retryWrites=true&w=majority' % (username, password))
#cluster = MongoClient('mongodb://root:rnsit%40123@rnsit-ecert.7ufby.mongodb.net/test?')
db = cluster["test"]
collection = db["certificates"]

# insert_one / insert_many

results = collection.find({"usn1":"1RN17EC060"})
for result in results:
    print(result["_id"])

print(results)

