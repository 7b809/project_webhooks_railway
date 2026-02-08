from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

sr_collection = db["sr_alerts"]
raw_collection = db["raw_alerts"]   # 🔥 NEW
