import time
from typing import List
from utils.logger import logger
from services.translation.base_translation_handler import BaseTranslationHandler
from data.entities import TranslationEntity, EvaluationLeafletData


class TestingTranslationHandler(BaseTranslationHandler):
    def __init__(self):
        super().__init__()



    def _process_translation(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        evaluation_leaflet_data: EvaluationLeafletData = kwargs.get('evaluation_leaflet_data')

        if evaluation_leaflet_data and self._is_translation_successful(translation):
            pass
          
            # translation.evaluation_scores = {}
        return translation


    async def _process_translation_async(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        evaluation_leaflet_data: EvaluationLeafletData = kwargs.get('evaluation_leaflet_data')

        if evaluation_leaflet_data and self._is_translation_successful(translation):
            pass

            # translation.evaluation_scores = {}
        return translation


    @staticmethod
    def _is_translation_successful(translation: TranslationEntity) -> bool:
        return (
            translation.metadata.get('status') != 'error' and
            translation.translated_text and
            translation.translated_text.strip() != ""
        )
