class searchEngine:
    
    def case_sensitive_search(self, db, query):
        docs = db.webpages.find({"$text": {"$search": query, "$caseSensitive": True}})
        urls = [doc['URL'] for doc in docs]
        return urls
         
    