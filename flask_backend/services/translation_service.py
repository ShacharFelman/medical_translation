from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from services.llm_initializer import initialize_translators
from evaluation.bleu_score import calculate_bleu
from database.mongodb_client import MongoDBClient
import time

class TranslationService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.translators = initialize_translators()
        self._initialized = False
        self.mongo_client = MongoDBClient.get_instance()

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, text_input, human_verified_translation=None):
            if not self.is_initialized():
                raise RuntimeError("TranslationService is not initialized")

            translations = []
            
            for translator in self.translators:
                start_time = time.time()
                translation = translator.translate(text_input)
                end_time = time.time()

                response_time = end_time - start_time
                bleu_score = None
                if human_verified_translation:
                    bleu_score = calculate_bleu(human_verified_translation, translation['content'])

                translation_data = {
                    'output': translation['content'],
                    'response_time': response_time,
                    'bleu_score': bleu_score,
                    'metadata': translation['metadata']
                }

                translations.append(translation_data)

            translation_record = {
                'input_text': text_input,
                'translations': translations,
                'timestamp': time.time()
            }

            # Save to MongoDB
            try:
                result = self.mongo_client.insert_translation(translation_record)
                logger.info(f"Translation saved to MongoDB with ID: {result.inserted_id}")
            except Exception as e:
                logger.error(f"Failed to save translation to MongoDB: {str(e)}")

            self.log_translation(translation_record)

            return translations[0]['output']

    def log_translation(self, data):
        logger.info(f"Translation request:")
        logger.info(f"Input text: {data['input_text']}")
        
        for translation in data['translations']:
            logger.info(f"Translator metadata: {translation['metadata']}")
            logger.info(f"Response time: {translation['response_time']:.2f} seconds")
            if translation['bleu_score'] is not None:
                logger.info(f"BLEU score: {translation['bleu_score']:.4f}")
            logger.info("---")

translation_service = TranslationService()