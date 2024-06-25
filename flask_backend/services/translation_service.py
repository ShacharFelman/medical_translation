from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from services.llm_initializer import initialize_translators
class TranslationService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.translators = initialize_translators()
        self._initialized = False

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, text_input):
        responses = []
        
        for translator in self.translators:    
            translation = translator.translate(text_input)
            responses.append(translation)

        for translation in responses:
            logger.debug("-------------------")
            # logger.debug(f'Translator: {translation["metadata"]}')
            logger.debug(f'Translation: {translation["content"]}')

        return responses[0]["content"]

translation_service = TranslationService()