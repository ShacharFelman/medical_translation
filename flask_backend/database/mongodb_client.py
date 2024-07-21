import os
from typing import Optional, Dict, Any, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from utils.logger import logger
from bson import ObjectId
from data.entities import TranslationRecordEntity, LeafletHistoryEntity

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
        try:
            result = self.collections['translation_history'].insert_one(leaflet_history.to_dict())
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert leaflet into MongoDB: {str(e)}")
            return None


    # def get_translation_history(self, leaflet_id: str) -> Optional[LeafletHistoryEntity]:
    #     try:
    #         result = self.collections['translation_history'].find_one({"id": leaflet_id})
    #         return LeafletHistoryEntity.from_dict(result) if result else None
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve leaflet from MongoDB: {str(e)}")
    #         return None

    def get_all_translation_history(self) -> List[LeafletHistoryEntity]:
        try:
            result = self.collections['translation_history'].find({}, {'_id': 0})  # Exclude MongoDB's _id field
            # logger.info(f'*****\n{result}\n*****')
            return [LeafletHistoryEntity.from_dict(doc) for doc in result]
        except Exception as e:
            logger.error(f"Failed to retrieve all leaflets from MongoDB: {str(e)}")
            return []

    def close(self):
        self.client.close()

    @staticmethod
    def get_client():
        return MongoDBClient.get_instance()