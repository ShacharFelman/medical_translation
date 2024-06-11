from langchain_openai import ChatOpenAI
from singleton_meta import SingletonMeta
from logger import logger
import os

from services.prompt_templates import translation_prompt

api_key = os.getenv('API_KEY_OPENAI')

class TranslationService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name='gpt-4o', temperature=0.0, api_key=api_key)
        # self.llm = llm
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
        # response = self._remove_translation_tags(response.content)
        return response.content

    def _remove_translation_tags(self, text: str) -> str:
        text = text.strip()
        logger.error('---' + text)
        if text.startswith("<eng_text>") and text.endswith("</eng_text>"):
            text = text.removeprefix("<eng_text>").removesuffix("</eng_text>")
            return text.strip()
        else:
            raise Exception(f"@@@@error in translation output: {text}")
