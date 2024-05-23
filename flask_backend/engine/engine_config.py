from singleton_meta import SingletonMeta

class EngineConfig(metaclass=SingletonMeta):
    file_cache_timeout_minutes = 1
    

engine_config = EngineConfig()

