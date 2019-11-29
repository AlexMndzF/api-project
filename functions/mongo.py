#!/usr/bin/python3

from pymongo import MongoClient
import getpass
import json
import os

#Get Password
password = getpass.getpass("Insert your AtlasMongoDB alexmendez password: ")
connection = f"mongodb+srv://alexmendez:{password}@cluster0-ugfnh.mongodb.net/test?retryWrites=true&w=majority"

#Connect to DB
client = MongoClient(connection)
def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll
