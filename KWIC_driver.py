#Importing the KWIC module
import pandas as pd
from KWIC import master
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

#clearing the collection
collection.delete_many({})
collection.drop_indexes()

#Creating the master object
KWIC = master(collection)

#Reading lines
df = pd.read_csv('website_classification_cleaned_filtered.csv')
print(df.head())

for i in range(70):
    row = df.iloc[i]
    url = row.iloc[0]
    content = row.iloc[1]
    KWIC.process_line(content, url)
    

#Create index on the circularly shifted lines
db.webpages.create_index([("Circular Shifts", "text")])
    
