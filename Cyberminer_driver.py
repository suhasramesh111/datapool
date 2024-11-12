#Importing Cyberminer.py
from Cyberminer import searchEngine

engine = searchEngine()

query = "indian foreign affairs"

urls = engine.case_sensitive_search(query)
urls.sort()

print(f"Results for the query - {query}: \n{urls}")
print()

# query = "indian"
# autofill = engine.autofill_search(query)
# print(f"Autofill results for the query - {query}: \n{autofill}")

