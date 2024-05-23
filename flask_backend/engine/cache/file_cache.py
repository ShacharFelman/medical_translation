from engine.cache.cache import Cache
from engine.utils.hash import create_string_hash
from logger import logger

class FileCache(Cache):
    def __init__(self,timeout_minutes=None):
        super().__init__(timeout_minutes)

    def get_file_data(self,file_name:str,file_content:str):
        self.remove_expired_entries()
        file_key = self.get_cache_key(file_name,file_content)
        reference_token = create_string_hash(file_key)
        cache_processed_data = self.get(reference_token)
        if not cache_processed_data:
            self.register_file(file_name,file_content)
        cache_processed_data = self.get(reference_token)
        return cache_processed_data

            # prcoessed_data = self.file_processor.process(file_name,file_content)
    def register_file(self,file_name:str,file_content:str,file_data):
        self.remove_expired_entries()
        file_key = self.get_cache_key(file_name,file_content)
        reference_token = create_string_hash(file_key)
        exist_token = self.get(reference_token)
        if not exist_token:
            self.add(reference_token,file_data,self._timeout_minutes)
        elif exist_token != reference_token:
            logger.error("file proccessing cache - shouldnt be here")
        return reference_token


    def get_cache_key(self,file_name:str,file_content:str):
        file_key = str(file_content.strip())
        return file_key