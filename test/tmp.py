import pandas as pd
import numpy as np
import time
from pymongo import MongoClient
from faker import Faker

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["big_titanic_db"]
collection = db["passengers"]

# Step 1: Load Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Step 2: Expand dataset to 1,000,000 rows
fake = Faker()
num_rows = 1000000
new_data = []

for _ in range(num_rows // len(df)):  # Duplicate original dataset
    temp_df = df.copy()
    temp_df["Name"] = [fake.name() for _ in range(len(temp_df))]  # Fake names
    temp_df["Age"] = np.random.randint(1, 90, size=len(temp_df))  # Random ages
    temp_df["Fare"] = np.random.uniform(5, 500, size=len(temp_df))  # Random fares
    new_data.append(temp_df)

# Convert to DataFrame
big_df = pd.concat(new_data, ignore_index=True)

# Convert DataFrame to dictionary for MongoDB
big_data = big_df.to_dict(orient="records")

# Step 3: Insert into MongoDB (Bulk insert for efficiency)
collection.insert_many(big_data)

# Verify insert count
print(f"Inserted {collection.count_documents({})} documents successfully!")

# Step 4: Query Survivors Without Indexing (Using Loop)
start_time = time.time()

survivors_list = []
for passenger in collection.find({"Survived": 1}):
    survivors_list.append(passenger)

survivor_count_loop = len(survivors_list)
time_loop = time.time() - start_time

print(f"\nSurvivor count (Without Indexing - Loop): {survivor_count_loop}")
print(f"Time taken (Without Indexing - Loop): {time_loop:.6f} seconds")

# Step 5: Create Index on 'Survived' Column
collection.create_index("Survived")

# Step 6: Query Survivors With Indexing (Using count_documents)
start_time = time.time()

survivor_count_indexed = collection.count_documents({"Survived": 1})
time_indexed = time.time() - start_time

print(f"\nSurvivor count (With Indexing - count_documents): {survivor_count_indexed}")
print(f"Time taken (With Indexing - count_documents): {time_indexed:.6f} seconds")

# Step 7: Performance Comparison
print("\nPerformance Comparison:")
print(f"Without Indexing (Loop): {time_loop:.6f} seconds")
print(f"With Indexing (count_documents): {time_indexed:.6f} seconds")
print(f"Speed Improvement: {time_loop / time_indexed:.2f}x faster with indexing!")
