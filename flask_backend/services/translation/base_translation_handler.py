from typing import List
import time
import asyncio
from utils.logger import logger
from services.translation.llm_manager import initialize_translators
from data.data_conversions import translator_llm_response_to_entity
from data.entities import TranslationEntity


class BaseTranslationHandler:
    def __init__(self):
        self.translators = initialize_translators()


    def translate(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        return self.translate_text(text_input, **kwargs)


    async def translate_async(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        return await self.translate_text_async(text_input, **kwargs)


    def translate_text(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        translations = [self._translate_with_model(translator, text_input, **kwargs) for translator in self.translators]
        return translations


    async def translate_text_async(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        tasks = [self._translate_with_model_async(translator, text_input, **kwargs) for translator in self.translators]
        translations = await asyncio.gather(*tasks)
        return translations


    def _translate_with_model(self, translator, text_input: str, **kwargs) -> TranslationEntity:
        start_time = time.time()
        try:
            llm_response = translator.translate(text_input)
            response_time = self._calc_response_time(start_time)
            translation = translator_llm_response_to_entity(llm_response, response_time)
            return self._process_translation(translation, text_input, **kwargs)
        except Exception as e:
            return self._handle_exception(e, translator.translator_name, start_time)
                

    async def _translate_with_model_async(self, translator, text_input: str, **kwargs) -> TranslationEntity:
        start_time = time.time()
        try:
            llm_response = await translator.translate_async(text_input)
            response_time = self._calc_response_time(start_time)
            translation = translator_llm_response_to_entity(llm_response, response_time)
            return await self._process_translation_async(translation, text_input, **kwargs)
        except Exception as e:
            return self._handle_exception(e, translator.translator_name, start_time)


    def _process_translation(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        pass


    async def _process_translation_async(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        pass
    

    def _calc_response_time(self, start_time: float) -> float:
        return time.time() - start_time


    def _handle_exception(self, e: Exception, translator_name: str, start_time: float) -> TranslationEntity:
        response_time = self._calc_response_time(start_time)
        logger.error(f"Error translating with translator {translator_name}: {str(e)}")
        return self._create_error_response(str(e), translator_name, response_time)


    def _create_error_response(self, error_message: str, translator_name: str, response_time: float) -> TranslationEntity:
        return TranslationEntity(
            translator_name=translator_name,
            translated_text="",
            response_time=response_time,
            metadata={"status": "error", "error_message": error_message}
        )
