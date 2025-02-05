from pymongo import MongoClient

# Connect to MongoDB (make sure MongoDB is running locally on port 27017)
client = MongoClient("mongodb+srv://reejubhattacherji7:eHnnVv7hMR3H39LL@test-cluster.qi63c.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster")

# # Create or access the database
# db = client["university_db"]

# # Create collections (tables in SQL terms)
# students_collection = db["students"]
# courses_collection = db["courses"]

# # Sample data for students collection
# students_data = [
#     {"student_id": 1, "name": "Alice", "age": 21, "major": "Computer Science"},
#     {"student_id": 2, "name": "Bob", "age": 22, "major": "Mathematics"},
#     {"student_id": 3, "name": "Charlie", "age": 23, "major": "Physics"},
#     {"student_id": 4, "name": "David", "age": 20, "major": "Chemistry"},
#     {"student_id": 5, "name": "Eve", "age": 21, "major": "Biology"},
#     {"student_id": 6, "name": "Frank", "age": 22, "major": "Economics"},
#     {"student_id": 7, "name": "Grace", "age": 24, "major": "History"},
#     {"student_id": 8, "name": "Hank", "age": 25, "major": "Philosophy"},
#     {"student_id": 9, "name": "Ivy", "age": 21, "major": "Political Science"},
#     {"student_id": 10, "name": "Jack", "age": 23, "major": "Engineering"}
# ]

# # Sample data for courses collection
# courses_data = [
#     {"course_id": "CS101", "course_name": "Intro to CS", "credits": 3},
#     {"course_id": "MATH201", "course_name": "Calculus I", "credits": 4},
#     {"course_id": "PHYS301", "course_name": "Quantum Physics", "credits": 4},
#     {"course_id": "CHEM101", "course_name": "Organic Chemistry", "credits": 3},
#     {"course_id": "BIO202", "course_name": "Genetics", "credits": 3},
#     {"course_id": "ECON303", "course_name": "Macroeconomics", "credits": 3},
#     {"course_id": "HIST101", "course_name": "World History", "credits": 3},
#     {"course_id": "PHIL102", "course_name": "Ethics", "credits": 3},
#     {"course_id": "POLSCI201", "course_name": "International Relations", "credits": 3},
#     {"course_id": "ENGG101", "course_name": "Mechanical Engineering", "credits": 4}
# ]

# # Insert data into collections
# students_collection.insert_many(students_data)
# courses_collection.insert_many(courses_data)

# print("Data inserted successfully!")

# # Verify inserted data
# print("\nStudents Collection:")
# for student in students_collection.find():
#     print(student)

# print("\nCourses Collection:")
# for course in courses_collection.find():
#     print(course)

# reejubhattacherji7
# eHnnVv7hMR3H39LL

import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB (Ensure MongoDB is running)
# client = MongoClient("mongodb://localhost:27017/")
db = client["titanic_db"]  # Create or access the database
collection = db["passengers"]  # Create or access the collection

# # Load Titanic dataset from an online source
# url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
# df = pd.read_csv(url)

# # Convert DataFrame to dictionary format (for MongoDB)
# data_dict = df.to_dict(orient="records")

# # Insert data into MongoDB
# collection.insert_many(data_dict)

# print("Titanic dataset uploaded successfully!")

# # Verify by printing a few documents
# print("\nSample Data from MongoDB:")
# for doc in collection.find().limit(5):
#     print(doc)


# new_passenger = {
#     "Name": "John Doe",
#     "Pclass": 1,
#     "Age": 35,
#     "Sex": "male",
#     "Survived": 1,
#     "Fare": 75.0,
#     "Embarked": "S",
#     "SibSp": 0,
#     "Parch": 0
# }
# result = collection.insert_one(new_passenger)
# print(f"Inserted document ID: {result.inserted_id}")


# passengers = [
#     {"Name": "Jane Doe", "Pclass": 2, "Age": 28, "Sex": "female", "Survived": 1, "Fare": 50.0, "Embarked": "C", "SibSp": 0, "Parch": 0},
#     {"Name": "Alex Smith", "Pclass": 3, "Age": 40, "Sex": "male", "Survived": 0, "Fare": 10.0, "Embarked": "Q", "SibSp": 1, "Parch": 2}
# ]
# result = collection.insert_many(passengers)
# print(f"Inserted document IDs: {result.inserted_ids}")


# for passenger in collection.find({"Survived": 1, "Pclass": 1}):
#     print(passenger)


# collection.update_one({"Name": "John Doe"}, {"$set": {"Fare": 100.0}})
# print("Updated John Doe's fare.")


# collection.delete_one({"Name": "John Doe"})
# print("Deleted John Doe.")


import time 

start_time = time.time()  # Start time tracking

# Retrieve all survivors and store them in a list
survivors_list = []
for passenger in collection.find({"Survived": 1}):
    survivors_list.append(passenger)

survivor_count_loop = len(survivors_list)  # Count survivors

end_time = time.time()  # End time tracking
time_loop = end_time - start_time  # Calculate time taken

print(f"Survivor count using loop: {survivor_count_loop}")
print(f"Time taken using loop: {time_loop:.6f} seconds")


start_time = time.time()  # Start time tracking

# Get the survivor count using MongoDB’s built-in function
survivor_count_builtin = collection.count_documents({"Survived": 1})

end_time = time.time()  # End time tracking
time_builtin = end_time - start_time  # Calculate time taken

print(f"Survivor count using inbuilt function: {survivor_count_builtin}")
print(f"Time taken using inbuilt function: {time_builtin:.6f} seconds")



print("\nPerformance Comparison:")
print(f"Loop Approach Time: {time_loop:.6f} seconds")
print(f"Inbuilt Function Time: {time_builtin:.6f} seconds")
print(f"Speed Improvement: {time_loop / time_builtin:.2f}x faster using count_documents()")

collection.create_index
