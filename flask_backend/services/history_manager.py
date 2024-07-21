from typing import Optional, List
from utils.logger import logger
from data.boundaries import LeafletSaveRequest, FetchLeafletsResponse
from database.mongodb_client import MongoDBClient
from utils.singleton_meta import SingletonMeta
from data.data_conversions import leaflet_save_request_to_entity, leaflet_history_entity_to_save_request, leaflet_history_entity_to_response

class HistoryManager(metaclass=SingletonMeta):
    def __init__(self):
        self.mongo_client = MongoDBClient.get_instance()

    def save_leaflet(self, save_request: LeafletSaveRequest) -> Optional[str]:
        try:
            logger.info(f"Saving leaflet request: {save_request}")
            leaflet_history = leaflet_save_request_to_entity(save_request)
            logger.info(f"Saving leaflet: {leaflet_history}")
            result = self.mongo_client.insert_translation_history(leaflet_history)
            
            if result:
                logger.info(f"Leaflet saved successfully with ID: {leaflet_history.id}")
                return leaflet_history.id
            else:
                logger.error("Failed to save leaflet to database")
                return None
        except Exception as e:
            logger.error(f"Error saving leaflet to history: {str(e)}")
            return None
        
    def fetch_all_leaflets(self) -> FetchLeafletsResponse:
        try:
            leaflet_entities = self.mongo_client.get_all_translation_history()
            leaflets = [leaflet_history_entity_to_response(entity) for entity in leaflet_entities]
            
            return FetchLeafletsResponse(leaflets=leaflets)
        except Exception as e:
            logger.error(f"Error fetching all leaflets: {str(e)}")
            return FetchLeafletsResponse(leaflets=[])
        
#     # TODO: change id logic
    # def get_leaflet_history(self, leaflet_id: str) -> Optional[LeafletSaveRequest]:
    #     try:
    #         leaflet_entity = self.mongo_client.get_translation_history(leaflet_id)
            
    #         if leaflet_entity:
    #             return leaflet_history_entity_to_save_request(leaflet_entity)
    #         else:
    #             logger.warning(f"No leaflet found with ID: {leaflet_id}")
    #             return None
    #     except Exception as e:
    #         logger.error(f"Error retrieving leaflet history: {str(e)}")
    #         return None

history_manager = HistoryManager()






