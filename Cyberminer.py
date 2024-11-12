from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_USER, MONGO_PASS, MONGO_DB, MONGO_APP
import re

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
    
    
    def autofill_search(self, query, limit=5):
        # Simple regex to match the query word and the next 1-2 words after it
        regex = rf"\b{re.escape(query)}\b(?:\s+(\w+))?(?:\s+(\w+))?"
    
        # Query the database for a single document matching the regex pattern
        doc = self.db.webpages.find_one({"Circular Shifts": {"$regex": regex, "$options": "i"}})
        
        if not doc:
            return []  
        
        cs = doc['Circular Shifts'][0]  
        matches = re.findall(regex, cs)
    
        suggestions = []
        
        for match in matches:
            next_words = [word for word in match if word]
            suggestions.extend(next_words)
        
        # Return unique suggestions, limit the number of suggestions
        return list(set(suggestions))[:limit]
    
        
             
        