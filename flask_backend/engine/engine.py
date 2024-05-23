from engine.models.claude import claude_translation_model_instance
# from medical_translation.flask_backend.engine.cache.cache import Cache
# from medical_translation.flask_backend.engine.file_handling.files_processor import FileProcessor
from singleton_meta import SingletonMeta
from engine.engine_config import EngineConfig,engine_config
from logger import logger

_translation_model = claude_translation_model_instance


class Engine(metaclass=SingletonMeta):
    def __init__(self,translation_model, engine_config:EngineConfig) -> None:
        self.config = engine_config 
        self.translation_model = translation_model 
        # self.cache = Cache(engine_config.file_cache_timeout_minutes)
        self._initialized = False

    def initialize(self):
        self._initialized = True

    def is_initialized(self):
        return self._initialized 

    def translate(self,reference_data,dest_lang,source_lang,text_input,html_input):
        logger.debug(f'****************** \n{text_input}\n *******************') 
        response = self.translation_model.translate_paragraph(text_input,html_input,reference_data) # reference data TODO
        logger.debug(f'####################### \n{response}\n #######################') 
        response = self.translation_model.remove_translation_tags(response)
        return response


    # def get_processed_file_data(self,filename,text):
    #     self.cache.remove_expired_entries()
    #     file_key = self.get_cache_key(filename,text)
    #     reference_token = create_file_hash_id_from_key(file_key)
    #     cache_processed_data = self.cache.get(reference_token)
    #     if not cache_processed_data:
    #         self.register_reference_file(filename,text)
    #     cache_processed_data = self.cache.get(reference_token)
    #     return cache_processed_data


    # def register_reference_file(self,filename,text):
    #     self.cache.remove_expired_entries()
    #     file_key = self.get_cache_key(filename,text)
    #     reference_token = create_file_hash_id_from_key(file_key)
    #     exist_token = self.cache.get(reference_token)
    #     if not exist_token:
    #         prcoessed_data = self.file_processor.process(filename,text)
    #         self.cache.add(reference_token,prcoessed_data,self.timeout_minutes)
    #     elif exist_token != reference_token:
    #         pass
    #     return reference_token


    # def get_cache_key(self,filename,text):
    #     file_key = str(text)
    #     return file_key


translation_engine = Engine(_translation_model ,engine_config)