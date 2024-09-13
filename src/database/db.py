from dotenv import load_dotenv
from os import getenv
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
MONGO_URL = getenv('MONGO_URL')

client = MongoClient(MONGO_URL, server_api=ServerApi('1'), tlsCAFile=certifi.where())

db = client.chatstore

collection = db['chathistory']