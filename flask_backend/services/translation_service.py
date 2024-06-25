from utils.singleton_meta import SingletonMeta
from utils.logger import logger
from services.llms.llm_initializer import initialize_llms
from services.prompt_templates import translation_prompt, translation_parser
from services.best_translation import transltion_selector
class TranslationService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.translators = []
        self.llms = initialize_llms()
        for llm in self.llms:
            self.translators.append(self._create_translator(llm))
        self._initialized = False

    def _create_translator(self, llm):
        chain = translation_prompt | llm
        return chain

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, text_input):
        responses = []
        
        for translator in self.translators:    
            response = translator.invoke({
                "text_input": text_input,
            })
            responses.append(response)

        for translation in responses:
            logger.debug("-------------------")
            logger.debug(f'Translator: {translation.response_metadata}')
            # logger.debug("Translated text:", translation.content)

        translations = [translation_parser.parse(response.content) for response in responses]    
        transltion_selector.select_best_translation(translations)

        return responses[0].content

translation_service = TranslationService()

