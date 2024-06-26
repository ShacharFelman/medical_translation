from pymongo import MongoClient
import os

class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
            self.client = MongoClient(mongodb_uri)
            self.db = self.client['translation_db']
            self.collection = self.db['translation_results']
            MongoDBClient._instance = self

    def insert_translation(self, data):
        return self.collection.insert_one(data)

    def get_translation(self, id):
        return self.collection.find_one({"_id": id})

    def close(self):
        self.client.close()