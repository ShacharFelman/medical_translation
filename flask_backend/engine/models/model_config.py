from singleton_meta import SingletonMeta

class ModelConfig(metaclass=SingletonMeta):
    MAX_TOKENS_LIMIT = 1024
    DEVICE="cpu"

model_config = ModelConfig()

