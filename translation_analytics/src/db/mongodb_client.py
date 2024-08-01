from pymongo import MongoClient
from typing import List, Dict, Any

class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['translation_performance']

    def get_all_records(self) -> List[Dict[str, Any]]:
        return list(self.collection.find())

    def get_records_by_date_range(self, start_date, end_date) -> List[Dict[str, Any]]:
        return list(self.collection.find({
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }))

    def get_records_by_translator(self, translator_name: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({
            "translations.translator_name": translator_name
        }))

    def get_records_by_leaflet(self, leaflet_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({
            "evaluation_leaflet_data.leaflet_id": leaflet_id
        }))