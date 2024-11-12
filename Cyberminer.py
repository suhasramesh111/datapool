from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_USER, MONGO_PASS, MONGO_DB, MONGO_APP

class searchEngine:
    def __init__(self):
        uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_DB}.yggrl.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_APP}"
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = client[MONGO_APP]
        
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        print()
    
    def case_sensitive_search(self, query):
        docs = self.db.webpages.find({"$text": {"$search": query, "$caseSensitive": True}})
        urls = [doc['URL'] for doc in docs]
        return urls
         
    