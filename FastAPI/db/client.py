from pymongo import MongoClient


# Base de datos local
# db_client = MongoClient(username='root', password='example').local

# Base de datos remota
db_client = MongoClient(username="root", password="example", host="test_mongo:27017").local

