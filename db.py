from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

students = db["students"]
users = db["users"]
marks = db["marks"]


def check_connection():
    client.admin.command("ping")


def init_indexes():
    students.create_index([("roll_number", ASCENDING)], unique=True)
    users.create_index([("roll_number", ASCENDING)], unique=True)
    marks.create_index([("roll_number", ASCENDING), ("semester", ASCENDING)], unique=True)