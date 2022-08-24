#!/usr/bin/python3
 
import pymongo
from pymongo import MongoClient

def get_collection():
    #client = MongoClient()
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclient.list_database_names()
    if "runoobdb" in db:
        print("database deja exist！")
  
    # collection = db.python_collection
    hives = db.hives
    return hives

def check_exist(coll,data):
    query_filter = {'name': data['name']}
    cnt = coll.find(query_filter).count()
    return cnt > 0

def page_query(query_filter=None, page_size, page_on=1):
    skip = page_size * (page_on - 1)
    coll = get_collection()
    page_record = coll.find(query_filter).limit(page_size).skip(skip)
    
    for r in page_record:
        print r
        
#if __name__ == "__main__":
     








  
