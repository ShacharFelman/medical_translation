from typing import List
from data.entities import TranslationEntity
from services.translation.base_translation_handler import BaseTranslationHandler


class RuntimeTranslationHandler(BaseTranslationHandler):  
    def _process_translation(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        # For runtime, we don't perform any additional processing
        return translation


    async def _process_translation_async(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        # For runtime, we don't perform any additional processing
        return translation