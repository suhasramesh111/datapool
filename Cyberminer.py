from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_USER, MONGO_PASS, MONGO_DB, MONGO_APP
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class SearchEngine:
    def __init__(self):
        uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_DB}.yggrl.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_APP}"
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = client[MONGO_APP]
        
        try:
            client.admin.command('ping')
            print("Pinged your deployment. Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def case_sensitive_search(self, query):
        """Performs a case-sensitive search and returns URLs and original content."""
        docs = self.db.webpages.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        )
        return [(doc['URL'], doc['score'], doc['Original content']) for doc in docs]

    # def autofill_search(self, query, limit=5):
    #     """Suggests autofill options based on the query."""
    #     regex = rf"\b{re.escape(query)}\b(?:\s+(\w+))?(?:\s+(\w+))?"
    #     doc = self.db.webpages.find_one({"Circular Shifts": {"$regex": regex, "$options": "i"}})
    #     if not doc:
    #         return []
    #     matches = re.findall(regex, doc['Circular Shifts'][0])
    #     suggestions = {word for match in matches for word in match if word}
    #     return list(suggestions)[:limit]

    def delete_out_of_date(self):
        """Delete documents from the database that are out of date (placeholder)."""
        pass

    def parallel_search(self, queries, search_func, *args, max_workers=5):
        """Perform parallel execution of a search function over multiple queries."""
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_query = {executor.submit(search_func, query, *args): query for query in queries}
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    results.append((query, result))
                except Exception as e:
                    print(f"Error processing query '{query}': {e}")
        return results
