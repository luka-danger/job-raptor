import pandas as pd

## Load Kaggle dataset
data = pd.read_csv("data/fake_job_postings.csv")
# Test data 
print(data.head())  # Print the first few rows to verify

## Clean Data
# Drop duplicates
data.drop_duplicates(inplace=True)  # Or data = data.drop_duplicates()



