import os
from typing import Optional, Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from data.entities import TranslationRecordEntity, LeafletHistoryEntity
from bson import ObjectId

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
            self.mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
            self.db_name = os.getenv('MONGODB_DB_NAME', 'translation_db')
            self.client = MongoClient(self.mongodb_uri, maxPoolSize=50, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.db_name]
            
            # Define collections
            self.collections = {
                'translation_performance': self.db['translation_performance'],
                'translation_history': self.db['translation_history']
            }
            
            MongoDBClient._instance = self

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        if collection_name not in self.collections:
            raise ValueError(f"Collection {collection_name} does not exist")
        
        try:
            result = self.collections[collection_name].insert_one(document)
            return str(result.inserted_id)
        except (ConnectionFailure, OperationFailure) as e:
            print(f"Failed to insert document into {collection_name}: {e}")
            return None

    def get_document(self, collection_name: str, id: str) -> Optional[Dict[str, Any]]:
        if collection_name not in self.collections:
            raise ValueError(f"Collection {collection_name} does not exist")
        
        try:
            result = self.collections[collection_name].find_one({"_id": ObjectId(id)})
            return result
        except (ConnectionFailure, OperationFailure) as e:
            print(f"Failed to retrieve document from {collection_name}: {e}")
            return None

    def insert_translation_performance(self, translation_record: TranslationRecordEntity) -> Optional[str]:
        return self.insert_document('translation_performance', translation_record.model_dump())

    def get_translation_performance(self, id: str) -> Optional[TranslationRecordEntity]:
        result = self.get_document('translation_performance', id)
        if result:
            return TranslationRecordEntity.from_dict(result)
        return None

    def insert_translation_history(self, leaflet_history: LeafletHistoryEntity) -> Optional[str]:
        return self.insert_document('translation_history', leaflet_history.to_dict())

    def get_translation_history(self, id: str) -> Optional[LeafletHistoryEntity]:
        result = self.get_document('translation_history', id)
        if result:
            return LeafletHistoryEntity.from_dict(result)
        return None

    def close(self):
        self.client.close()

    @staticmethod
    def get_client():
        return MongoDBClient.get_instance()