from typing import List, Optional
import time
from utils.logger import logger
from services.translation.llm_manager import initialize_translators
from data.data_conversions import translator_llm_response_to_entity
from data.entities import TranslationEntity


class BaseTranslationHandler:
    def __init__(self):
        self.translators = initialize_translators()

    def translate_text(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        translations = []
        for translator in self.translators:
            translation = self._translate_with_model(translator, text_input)
            translations.append(translation)
        return translations

    def _translate_with_model(self, translator, text_input: str) -> TranslationEntity:
        start_time = time.time()
        try:
            llm_response = translator.translate(text_input)
            end_time = time.time()
            response_time = end_time - start_time
            return translator_llm_response_to_entity(llm_response, response_time)
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            logger.error(f"Error translating with translator {translator.translator_name}: {str(e)}")
            return TranslationEntity(
                translator_name=translator.translator_name,
                translated_text="",
                response_time=response_time,
                metadata={"status": "error", "error_message": str(e)}
            )
    