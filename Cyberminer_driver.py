#Importing Cyberminer.py
from Cyberminer import searchEngine

engine = searchEngine()

query = "Indian foreign affairs"

urls = engine.case_sensitive_search(query)
sorted_urls = sorted(urls, key=lambda x: x[1], reverse=True)

print(f"Results for the query - {query}: \n{sorted_urls}")
print()

query = "indian launch"
autofill = engine.autofill_search(query)
print(f"Autofill results for the query - {query}: \n{autofill}")

