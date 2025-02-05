import pandas as pd
import numpy as np
import time
from pymongo import MongoClient
from faker import Faker

# Connect to MongoDB
client = MongoClient("mongodb+srv://reejubhattacherji7:eHnnVv7hMR3H39LL@test-cluster.qi63c.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster")
# client = MongoClient("mongodb://localhost:27017/")
db = client["big_titanic_db"]
collection = db["passengers"]

# Step 1: Load Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Step 2: Expand dataset to 1,000,000 rows
fake = Faker()
num_rows = 10000000
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

# Step 4: Pick a Random Name from Database to Search
random_person = collection.find_one({}, {"Name": 1})  # Get a random name
if random_person:
    target_name = random_person["Name"]
    print(f"\nSearching for: {target_name}")
else:
    print("No documents found in the collection.")
    target_name = None

# Step 5: Search Without Indexing (Using Loop)
start_time = time.time()

found_person_loop = None
for passenger in collection.find():
    if passenger["Name"] == target_name:
        found_person_loop = passenger
        break

time_loop = time.time() - start_time

print(f"\nPerson found (Without Indexing - Loop): {found_person_loop}")
print(f"Time taken (Without Indexing - Loop): {time_loop:.6f} seconds")

# Step 6: Create Index on 'Name' Column
collection.create_index("Name")

# Step 7: Search With Indexing (Using find_one)
start_time = time.time()

found_person_indexed = collection.find_one({"Name": target_name})

time_indexed = time.time() - start_time

print(f"\nPerson found (With Indexing - find_one): {found_person_indexed}")
print(f"Time taken (With Indexing - find_one): {time_indexed:.6f} seconds")

# Step 8: Performance Comparison
print("\nPerformance Comparison:")
print(f"Without Indexing (Loop): {time_loop:.6f} seconds")
print(f"With Indexing (find_one): {time_indexed:.6f} seconds")
print(f"Speed Improvement: {time_loop / time_indexed:.2f}x faster with indexing!")
