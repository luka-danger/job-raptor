import pandas as pd
from pymongo import MongoClient

# Load Indeed Data Set
dataset_path = 'data/Indeed_10k.csv'
data = pd.read_csv(dataset_path)

# Clean Data
data = data.dropna()
data['description'] = data['description'].str.strip()
data['description'] = data['description'].str.lower()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
database = client['job_postings_db']
collection = database['postings']

# Refresg Database
# collection.delete_many({})

# Convert data to dictionary and upload to MongoDB
collection.insert_many(data.to_dict('records'))
print("Data successfully uploaded to MongoDB!")

# Fetch and print first 10 items of mongodb
documents = collection.find().limit(10)
for doc in documents:
    print(doc)