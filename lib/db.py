# lib/db.py

from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client and database
client = None
db = None

try:
    print(f"Connecting to MongoDB: {MONGO_URI}")
    client = MongoClient(MONGO_URI)
    db = client["Attendance_DB"]
    print("Successfully connected to MongoDB.")
except errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")


def get_db():
    return db


def close_connection():
    if client:
        client.close()
        print("MongoDB connection closed.")


# Example function to insert a document into a collection
def insert_document(collection_name, document):
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id


# Example function to find a document in a collection
def find_document(collection_name, query):
    collection = db[collection_name]
    document = collection.find_one(query)
    return document


# Example function to update a document in a collection
def update_document(collection_name, query, update):
    collection = db[collection_name]
    result = collection.update_one(query, {"$set": update})
    return result.modified_count


# Example function to delete a document from a collection
def delete_document(collection_name, query):
    collection = db[collection_name]
    result = collection.delete_one(query)
    return result.deleted_count


# Ensure the connection is closed when the script ends
import atexit

atexit.register(close_connection)

if __name__ == "__main__":
    # Test the connection
    if db is not None:
        print("Database connection is active.")
    else:
        print("Database connection is not active.")

    # Test the insert_document function
    document = {
        "NAME": "John Doe",
        "CITY": "New York",
        "ASSIGNED_CLIENT_ID": 12345,
        "ATTENDANCE": [],
        "STATUS": "Present",
    }
    worker_collection_name = "Worker_Data"
    result = insert_document(worker_collection_name, document)
    print(f"Inserted document ID: {result}")
