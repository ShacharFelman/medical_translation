import unittest
import json
from typing import Dict
from utils.logger import logger
from services.translation_manager import TranslationManager
from services.translation.testing_translation_handler import TestingTranslationHandler
from data.entities import EvaluationLeafletData
from data.boundaries import TranslationRequest

class TranslationAccuracyTest(unittest.TestCase):
    def setUp(self):
        self.testing_handler = TestingTranslationHandler()
        self.translation_manager = TranslationManager(self.testing_handler)
        self.translation_manager.initialize()
        with open('tests/test_data/leaflets/4-Maalox_tablets.json', 'r', encoding='utf-8') as f:
            self.leaflet_data = json.load(f)

    def test_full_leaflet_translation(self):
        for section in self.leaflet_data['sections']:
            self.translate_and_evaluate_section(section)
 

    def translate_and_evaluate_section(self, section: Dict) -> float:
        for item in section['data']:
            if 'heb' in item and 'eng' in item and item['heb'] != "" and item['eng'] != "":
                translation_request = TranslationRequest(
                    source='he',
                    dest='en',
                    textInput=item['heb']
                )
                leaflet_data = EvaluationLeafletData(
                    leaflet_id=self.leaflet_data['dir_index'],
                    leaflet_name=self.leaflet_data['title'],
                    section_number=section['section_num'],
                    array_location=section['data'].index(item),
                    human_translation=item['eng']
                )
                translation_response = self.translation_manager.translate(
                    translation_request, 
                    evaluation_leaflet_data=leaflet_data,
                    evaluate=True
                ).translated_text

if __name__ == '__main__':
    unittest.main()
