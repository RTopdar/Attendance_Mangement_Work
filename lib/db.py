# lib/db.py
from datetime import datetime, timedelta
from pymongo import MongoClient, errors
from dotenv import load_dotenv

import os
import atexit

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client and database
client = None
db = None

try:

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


# Create a Worker Schema that Fetches Teh Worker List from Mongo and Then Creates a New Dictionary with the Worker ID and Worker Name


def create_Worker_Schema():
    db = get_db()
    # Fetch all entries from the Worker_Data collection
    entries = list(db["Worker_Data"].find())

    worker_schema = []

    for entry in entries:
        worker_schema.append(
            {
                "Worker_ID": str(entry["_id"]),
                "Worker_Name": entry["NAME"],
                "Worker_Email": entry["EMAIL"],
                "STATUS": "",
            }
        )

    return worker_schema


# Create a new Attendance Entry
def create_Attendance_Entry(date=None):
    print(f"Creating Attendance Entry at {date}")
    db = get_db()
    current_time = datetime.now()
    ist_time = current_time + timedelta(hours=5, minutes=30)
    ist_date = ist_time.date()
    ist_iso_format = ist_date.isoformat()
    date_info = None
    if date is not None:
        print("Date is provided.")
        date_info = date
    else:
        print("Date is not provided.")
        date_info = ist_iso_format

    entry = db["Daily_Attendance"].find_one({"DATE": date_info})

    if entry is not None:
        print("Attendance entry already exists.")
        entry["_id"] = str(entry["_id"])
        return entry
    elif entry is None:
        print("Attendance entry does not exist.")
        workers = create_Worker_Schema()
        attendance = {
            "DATE": date_info,
            "WORKER_LIST": workers,
            "CLIENT_ID": "",
            "SIGNED_BY": "",
        }
        result = db["Daily_Attendance"].insert_one(attendance)
        print("Attendance entry created successfully.")
        new_entry = db["Daily_Attendance"].find_one({"_id": result.inserted_id})
        new_entry["_id"] = str(new_entry["_id"])
        return new_entry


if __name__ == "__main__":
    # Test the connection
    if db is not None:
        print("Database connection is active.")
    else:
        print("Database connection is not active.")

    create_Attendance_Entry()
