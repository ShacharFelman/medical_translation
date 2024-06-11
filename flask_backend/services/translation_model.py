from logger import logger

from services.prompt_templates import translation_prompt

class TranslationModel():
    def __init__(self, llm) -> None:
        self.llm = llm
        self.translation_chain = self._create_translation_chain()
        self._initialized = False

    def _create_translation_chain(self):
        chain = translation_prompt | self.llm
        return chain

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def translate(self, text_input):
        response = self.translation_chain.invoke({
            "text_input": text_input,
        })
        logger.error(response.response_metadata)
        return response.content