import time
from typing import List, Tuple, Optional

from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from database.mongodb_client import MongoDBClient
from services.translation.llm_manager import initialize_translators
from services.translation.translation_selector import translation_selector
from services.evaluation.bleu_score import calculate_bleu
from data.entities import TranslationEntity, TranslationRecordEntity
from data.boundaries import TranslationRequest, TranslationResponse
from data.data_conversions import translator_llm_response_to_entity, entity_to_frontend_response

class TranslationManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._initialized = False
        self.translators = initialize_translators()
        self.mongo_client = MongoDBClient.get_instance()

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, translation_request: TranslationRequest, human_verified_translation: Optional[str] = None) -> TranslationResponse:
        if not self.is_initialized():
            raise RuntimeError("TranslationManager is not initialized")

        try:
            all_translations = self._generate_translations(translation_request.text_input, human_verified_translation)
            successful_translations = [t for t in all_translations if t.metadata.get('status') != 'error']
            
            best_translation = None
            similarity_scores = []
            if successful_translations:
                best_translation, similarity_scores = translation_selector.select_best_translation(successful_translations)
                  
            translation_record = TranslationRecordEntity(
                input=translation_request.text_input,
                translations=all_translations,
                best_translation=best_translation
            )
            
            self._update_translation_scores(translation_record, similarity_scores)
            self._save_translation_to_db(translation_record)
            self._log_translation(translation_record)

            if best_translation:
                return entity_to_frontend_response(best_translation)
            else:
                return TranslationResponse(
                    translated_text="",
                    translator_used="",
                    confidence_score=0.0
                )

        except Exception as e:
            logger.error(f"Error in translate method: {str(e)}")
            raise

  
    def _generate_translations(self, text_input: str, human_verified_translation: Optional[str]) -> List[TranslationEntity]:
        translations = []
        for translator in self.translators:
            translation = self._translate_with_model(translator, text_input)
            if human_verified_translation:
                bleu_score = calculate_bleu(human_verified_translation, translation.output)
                translation.bleu_score = bleu_score
            translations.append(translation)
        return translations
    

    def _translate_with_model(self, translator, text_input: str) -> TranslationEntity:
        try:
            start_time = time.time()
            llm_response = translator.translate(text_input)
            end_time = time.time()
            response_time = end_time - start_time

            # Convert LLM response to TranslationEntity
            translation_entity = translator_llm_response_to_entity(llm_response, response_time)

            # If there was an error, log it
            if llm_response.status == "error" or not llm_response.translated_text:
                error_message = llm_response.metadata.get("error_message", "Unknown error")
                logger.error(f"Translation failed for translator {llm_response.translator_name}: {error_message}")

            return translation_entity

        except Exception as e:
            logger.error(f"Error translating with translator {translator.translator_name}: {str(e)}")
            # Create an error TranslationEntity
            return TranslationEntity(
                translator_name=translator.translator_name,
                translated_text="",
                response_time=0.0,
                metadata={"status": "error", "error_message": str(e)}
            )

    def _update_translation_scores(self, translation_record: TranslationRecordEntity, similarity_scores: List[float]):
        successful_translations = [t for t in translation_record.translations if t.metadata.get('status') != 'error']
        for translation, score in zip(successful_translations, similarity_scores):
            translation.score = float(score)


    def _save_translation_to_db(self, translation_record: TranslationRecordEntity):
        try:
            result = self.mongo_client.insert_translation_performance(translation_record)
            logger.info(f"Translation saved to MongoDB with ID: {result}")
        except Exception as e:
            logger.error(f"Failed to save translation to MongoDB: {str(e)}")


    def _log_translation(self, translation_record: TranslationRecordEntity):
        logger.info(f"Translation request:")
        logger.info(f"Input text: {translation_record.input}")
        
        for translation in translation_record.translations:
            logger.info(f"Translator: {translation.translator_name}")
            logger.info(f"Status: {translation.metadata.get('status', 'unknown')}")
            logger.info(f"Score: {translation.score:.4f}" if translation.score is not None else "Score: N/A")
            logger.info(f"Response time: {translation.response_time:.2f} seconds")
            if translation.bleu_score is not None:
                logger.info(f"BLEU score: {translation.bleu_score:.4f}")
            logger.info(f"Translator metadata: {translation.metadata}")
            logger.info("---")


translation_manager = TranslationManager()