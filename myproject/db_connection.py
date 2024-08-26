import pymongo

url = "mongodb+srv://abhishekshukla0700:LAbODlhzFJBZH7uk@cluster0.kursdso.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(url)
db  = client['marketplace_amazon']


# MONGODB_URL  = mongodb+srv://abhishekshukla0700:LAbODlhzFJBZH7uk@cluster0.kursdso.mongodb.net/?retryWrites=true&w=majority
# MONGODB_PASS= LAbODlhzFJBZH7uk
# MONGO_PORT = 27017
# MONGODB_USER = abhishekshukla0700
# MONGODB_DBNAME = ByteConnect
# PORT = 4000
# NODE_ENV = development