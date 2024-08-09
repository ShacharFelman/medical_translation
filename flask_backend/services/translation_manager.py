import asyncio
import os
from typing import List, Optional
from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from utils.exceptions import InvalidUserInputError
from database.mongodb_client import MongoDBClient
from services.translation.llm_manager import initialize_translators
from services.translation.translation_selector import translation_selector
from services.llm_security.input_validator import PromptInjectionDetector
from data.entities import TranslationEntity, TranslationRecordEntity, EvaluationLeafletData
from data.boundaries import TranslationRequest, TranslationResponse
from data.data_conversions import translation_entity_to_response
from services.translation.base_translation_handler import BaseTranslationHandler


class TranslationManager(metaclass=SingletonMeta):
    def __init__(self, handler: BaseTranslationHandler) -> None:
        self._initialized = False
        self.handler = handler
        self.translators = initialize_translators()
        self.mongo_client = MongoDBClient.get_instance()
        self.prompt_injection_detector = PromptInjectionDetector()
        self.use_async = os.getenv('ASYNC_TRANSLATE', '0').lower() in ('1', 'true', 'yes')



    def initialize(self):
        self._initialized = True


    def is_initialized(self):
        return self._initialized


    def translate(self, translation_request: TranslationRequest, evaluation_leaflet_data: Optional[EvaluationLeafletData] = None) -> TranslationResponse:
        if not self.is_initialized():
            raise RuntimeError("TranslationManager is not initialized")

        try:
            if not evaluation_leaflet_data:
                is_valid, error_message = self.prompt_injection_detector.validate_input(translation_request.textInput)
                if not is_valid:
                    logger.warning(f"Input validation failed: {error_message}")
                    
                    # Create a TranslationEntity to represent the failed validation
                    failed_translation = TranslationEntity(
                        translator_name="Input Validator",
                        translated_text=f"Error: {error_message}",
                        response_time=0.0,
                        score=0.0,
                        metadata={"status": "error", "error_message": error_message}
                    )
                    
                    # Save the failed attempt to the database
                    translation_record = TranslationRecordEntity(
                        input=translation_request.textInput,
                        translations=[failed_translation],
                        best_translation=None
                    )
                    self._save_translation_to_db(translation_record)
                    
                    raise InvalidUserInputError("Invalid Input")

            if self.use_async:
                all_translations = asyncio.run(self.handler.translate_async(translation_request.textInput, evaluation_leaflet_data=evaluation_leaflet_data))
            else:
                all_translations = self.handler.translate(translation_request.textInput, evaluation_leaflet_data=evaluation_leaflet_data)


            successful_translations = [t for t in all_translations if self._is_translation_successful(t)]
            
            if not successful_translations:
                logger.error("No successful translations were generated.")
                self._save_translation_to_db(TranslationRecordEntity(
                    input=translation_request.textInput,
                    translations=all_translations,
                    best_translation=None,
                    evaluation_leaflet_data=evaluation_leaflet_data
                ))
                return TranslationResponse(
                    translated_text="",
                    translator_used=""
                )

            try:
                best_translation, similarity_scores = translation_selector.select_best_translation(successful_translations)
                
                if not best_translation:
                    logger.error("Failed to select best translation.")
                    self._save_translation_to_db(TranslationRecordEntity(
                        input=translation_request.textInput,
                        translations=all_translations,
                        best_translation=None,
                        evaluation_leaflet_data=evaluation_leaflet_data

                    ))
                    return TranslationResponse(
                        translated_text="",
                        translator_used=""                    )
            except Exception as e:
                logger.error(f"Error in selecting best translation: {str(e)}")
                self._save_translation_to_db(TranslationRecordEntity(
                    input=translation_request.textInput,
                    translations=all_translations,
                    best_translation=None,
                    evaluation_leaflet_data=evaluation_leaflet_data

                ))
                return TranslationResponse(
                    translated_text="",
                    translator_used=""
                )

            translation_record = TranslationRecordEntity(
                input=translation_request.textInput,
                translations=all_translations,
                best_translation=best_translation,
                evaluation_leaflet_data=evaluation_leaflet_data

            )
            
            self._update_translation_scores(translation_record, similarity_scores)
            self._save_translation_to_db(translation_record)
            # self._log_translation(translation_record)

            return translation_entity_to_response(best_translation)
        
        except InvalidUserInputError as e:
            raise InvalidUserInputError("Invalid Input")


        except Exception as e:
            logger.error(f"Error in translate method: {str(e)}")
            return TranslationResponse(
                translated_text="",
                translator_used=""
            )

    def _update_translation_scores(self, translation_record: TranslationRecordEntity, similarity_scores: List[float]):
        successful_translations = [t for t in translation_record.translations if self._is_translation_successful(t)]
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
            logger.debug(f"Translator: {translation.translator_name}")
            logger.debug(f"Translated output: {'Valid' if translation.translated_text else 'Empty'}")
            logger.debug(f"Similarity Score: {translation.score:.4f}" if translation.score is not None else "Score: N/A")
            logger.debug(f"Response time: {translation.response_time:.2f} seconds")
            logger.debug(f"Translator metadata: {translation.metadata}")
            logger.debug("---")

    @staticmethod
    def _is_translation_successful(translation: TranslationEntity) -> bool:
        return (
            translation.metadata.get('status') != 'error' and
            translation.translated_text and
            translation.translated_text.strip() != ""
        )

# translation_manager = TranslationManager()