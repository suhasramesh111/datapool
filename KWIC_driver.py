#Importing the KWIC module
import pandas as pd
from KWIC import master

#Creating the master object
KWIC = master()

#Reading lines
df = pd.read_csv('website_classification_cleaned_filtered.csv')
print(df.head())

for i in range(70):
    row = df.iloc[i]
    url = row.iloc[0]
    content = row.iloc[1]
    KWIC.process_line(content, url)
    

#Create index on the circularly shifted lines
KWIC.db.webpages.create_index([("Circular Shifts", "text")])
    
