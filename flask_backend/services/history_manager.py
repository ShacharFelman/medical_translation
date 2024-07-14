from typing import Optional
from utils.logger import logger
from data.boundaries import LeafletSaveRequest
from data.entities import LeafletHistoryEntity
from database.mongodb_client import MongoDBClient
from utils.singleton_meta import SingletonMeta
from data.data_conversions import leaflet_save_request_to_entity, leaflet_history_entity_to_save_request

class HistoryManager(metaclass=SingletonMeta):
    def __init__(self):
        self.mongo_client = MongoDBClient.get_instance()

    def save_leaflet(self, save_request: LeafletSaveRequest) -> Optional[str]:
        try:
            leaflet_history = leaflet_save_request_to_entity(save_request)
            
            result = self.mongo_client.insert_translation_history(leaflet_history)
            
            if result:
                logger.info(f"Leaflet saved successfully with ID: {result}")
                return result
            else:
                logger.error("Failed to save leaflet to database")
                return None
        except Exception as e:
            logger.error(f"Error saving leaflet to history: {str(e)}")
            return None
        
    # TODO: check/change/implement/decide id logic
    def get_leaflet_history(self, leaflet_id: str) -> Optional[LeafletSaveRequest]:
        try:
            leaflet_entity = self.mongo_client.get_translation_history(leaflet_id)
            
            if leaflet_entity:
                return leaflet_history_entity_to_save_request(leaflet_entity)
            else:
                logger.warning(f"No leaflet found with ID: {leaflet_id}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving leaflet history: {str(e)}")
            return None

history_manager = HistoryManager()






