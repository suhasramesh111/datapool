#Importing Cyberminer.py
from Cyberminer import searchEngine
from pymongo import MongoClient
from pymongo.server_api import ServerApi

#Specifying DB connections
uri = "mongodb+srv://GeneralUser:GeneralUser@kwic-db.yggrl.mongodb.net/?retryWrites=true&w=majority&appName=KWIC-DB"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
print()

#Accessing Database
db = client["KWIC-DB"]
collection = db['webpages']

engine = searchEngine()

query = "indian foreign affairs"

urls = engine.case_sensitive_search(db, query)
urls.sort()

print(urls)
