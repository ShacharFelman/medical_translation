from engine.cache.file_cache import FileCache
from engine.engine_config import engine_config

file_cache = FileCache(engine_config.file_cache_timeout_minutes)