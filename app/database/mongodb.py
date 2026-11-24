
import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(MONGO_URL)

DATABASE_NAME = os.getenv(
    "MONGO_DATABASE",
    "customer_support_db"
)

database = client[DATABASE_NAME]

tickets_collection = database["tickets"]
users_collection = database["users"]
