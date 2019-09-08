import os
from pymongo import MongoClient


MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.job_ads
co_indeed = db.indeed





