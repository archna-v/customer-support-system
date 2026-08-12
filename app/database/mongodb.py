import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://localhost:27017"
)

client = MongoClient(MONGO_URL)

database = client["customer_support_db"]

tickets_collection = database["tickets"]
users_collection = database["users"]