from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from database.mongodb_client import MongoDBClient
from services.llm_initializer import initialize_translators
from services.translation_selector import translation_selector
from evaluation.bleu_score import calculate_bleu
import time

class TranslationService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.translators = initialize_translators()
        self.mongo_client = MongoDBClient.get_instance()
        self._initialized = False

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, text_input, human_verified_translation=None):
        if not self.is_initialized():
            raise RuntimeError("TranslationService is not initialized")

        translations_output = self._generate_translations(text_input, human_verified_translation)
        best_translation, similarity_scores = translation_selector.select_best_translation(translations_output)
        
        translation_record = self._prepare_translation_record(text_input, translations_output, best_translation, similarity_scores)
        self._save_translation_to_db(translation_record)
        self._log_translation(translation_record)

        return best_translation['output']


    def _generate_translations(self, text_input, human_verified_translation):
        translations_output = []
        for translator in self.translators:
            translation = self._translate_with_model(translator, text_input, human_verified_translation)
            translations_output.append(translation)
        return translations_output


    def _translate_with_model(self, translator, text_input, human_verified_translation):
        start_time = time.time()
        translation = translator.translate(text_input)
        end_time = time.time()
        response_time = end_time - start_time

        if human_verified_translation:
            bleu_score = calculate_bleu(human_verified_translation, translation['content'])

        return {
            'model_name': translation['model_name'],
            'output': translation['content'],
            'response_time': response_time,
            'bleu_score': bleu_score,
            'metadata': translation['metadata']
        }


    def _prepare_translation_record(self, text_input, translations_output, best_translation, similarity_scores):
        translations = [
            {**translation, 'score': float(score)}
            for translation, score in zip(translations_output, similarity_scores)
        ]

        return {
            'input': text_input,
            'translations': translations,
            'best_translation': best_translation,
            'timestamp': time.time()
        }


    def _save_translation_to_db(self, translation_record):
        try:
            result = self.mongo_client.insert_translation(translation_record)
            logger.info(f"Translation saved to MongoDB with ID: {result.inserted_id}")
        except Exception as e:
            logger.error(f"Failed to save translation to MongoDB: {str(e)}")


    def _log_translation(self, data):
        logger.info(f"Translation request:")
        logger.info(f"Input text: {data['input']}")
        
        for translation in data['translations']:
            logger.info(f"Translator: {translation['model_name']}")
            logger.info(f"score: {translation['score']:.4f}")
            logger.info(f"Response time: {translation['response_time']:.2f} seconds")
            if translation['bleu_score'] is not None:
                logger.info(f"BLEU score: {translation['bleu_score']:.4f}")
            logger.info(f"Translator metadata: {translation['metadata']}")
            logger.info("---")


translation_service = TranslationService()