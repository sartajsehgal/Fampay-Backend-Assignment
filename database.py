from flask import Flask
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://sartaj16:sartaj2000@cluster0.stns21q.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('Videos')
user_collection = pymongo.collection.Collection(db, 'VideosInfo')