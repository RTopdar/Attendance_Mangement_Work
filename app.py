# app.py
from crypt import methods
from email import message
from flask import Flask, request, jsonify
from lib.db import create_Attendance_Entry, get_db

app = Flask(__name__)


@app.route("/")
def home():
    db = get_db()
    if db is not None:
        return "Connected to MongoDB"
    return "Attendance App Version 0.0.1"


@app.route("/workers/get_attendance_entry", methods=["GET"])
def get_attendance_entry():
    date = request.args.get("date")

    if date is None:
        return jsonify({"message": "Date is required."}), 400
    

    WORKER_DATA = create_Attendance_Entry(date)

    return jsonify(
        {
            "message": "Attendance Entry Created/Fetched Successfully",
            "WORKER_DATA": WORKER_DATA,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
