import unittest
from typing import List
from tqdm import tqdm
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, TranslationEntity, EvaluationLeafletData
from services.translation_manager import TranslationManager
from services.translation.testing_translation_handler import TestingTranslationHandler
from data.boundaries import TranslationRequest
from utils.logger import logger

class FilteredTranslationUpdater(unittest.TestCase):
    def setUp(self):
        self.mongo_client = MongoDBClient.get_instance()
        self.testing_handler = TestingTranslationHandler()
        self.translation_manager = TranslationManager(self.testing_handler)
        self.translation_manager.initialize()


    def test_update_translations(self):
        all_records = self.get_all_records_from_db()
        filtered_records: List[TranslationRecordEntity] = self.filter_records_with_heb_text(all_records)
        
        for record in tqdm(filtered_records, desc="Updating translations"):
            if record.translations:
                logger.info(f"========== Leaflet {record.evaluation_leaflet_data.leaflet_id}, Section {record.evaluation_leaflet_data.section_number}, Array Location {record.evaluation_leaflet_data.array_location} ==========")
                self.translate_and_evaluate(record)
                logger.info(f"Record translation updated")
                
            
    def get_all_records_from_db(self) -> List[TranslationRecordEntity]:
        all_records = self.mongo_client.get_all_translation_records()
        logger.info(f"Retrieved {len(all_records)} records from the database")
        return all_records


    #Filter records with missing translations
    def filter_records_with_missing_translations(self, records: List[TranslationRecordEntity]) -> List[TranslationRecordEntity]:
        filtered_records = []
        for record in records:
            if record.translations:
                for translation in record.translations:
                    if (not translation.translated_text or translation.translated_text.strip() == ""):
                        logger.info(f"Missing translation found for model {translation.translator_name}")
                        filtered_records.append(record)
                        break
        logger.info(f"Found {len(filtered_records)} records with missing translations")
        return filtered_records


    #Filter records with <heb_text> tags
    def filter_records_with_heb_text(self, records: List[TranslationRecordEntity]) -> List[TranslationRecordEntity]:
        filtered_records = []
        for record in records:
            if record.translations:
                for translation in record.translations:
                    if ("<heb_text>" in translation.translated_text):
                        logger.info(f"<heb_text> found for model {translation.translator_name}")
                        filtered_records.append(record)
                        break
        logger.info(f"Found {len(filtered_records)} records with missing translations")
        return filtered_records



    def translate_and_evaluate(self, translation_recore: TranslationRecordEntity) -> float:
        translation_request = TranslationRequest(
            source='he',
            dest='en',
            textInput=translation_recore.input
        )

        leaflet_data = EvaluationLeafletData(
            leaflet_id=translation_recore.evaluation_leaflet_data.leaflet_id,
            leaflet_name=translation_recore.evaluation_leaflet_data.leaflet_name,
            section_number=translation_recore.evaluation_leaflet_data.section_number,
            array_location=translation_recore.evaluation_leaflet_data.array_location,
            human_translation=translation_recore.evaluation_leaflet_data.human_translation
        )

        self.translation_manager.translate(
            translation_request, 
            evaluation_leaflet_data=leaflet_data
        )


if __name__ == '__main__':
    unittest.main()