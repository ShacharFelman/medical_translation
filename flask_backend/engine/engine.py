from engine.models.claude import claude_translation_model_instance
from singleton_meta import SingletonMeta
from engine.engine_config import EngineConfig,engine_config
from logger import logger

_translation_model = claude_translation_model_instance


class Engine(metaclass=SingletonMeta):
    def __init__(self,translation_model, engine_config:EngineConfig) -> None:
        self.config = engine_config 
        self.translation_model = translation_model 
        self._initialized = False

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized 

    def translate(self,dest_lang,source_lang,text_input,html_input):
        response = self.translation_model.translate_paragraph(text_input,html_input)
        response = self.translation_model.remove_translation_tags(response)
        return response

translation_engine = Engine(_translation_model ,engine_config)