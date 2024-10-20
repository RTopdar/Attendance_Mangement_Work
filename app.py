# app.py
from flask import Flask
from lib.db import get_db

app = Flask(__name__)


@app.route("/")
def home():
    db = get_db()
    return "Attendance App Version 0.0.1"


if __name__ == "__main__":
    app.run(debug=True)
