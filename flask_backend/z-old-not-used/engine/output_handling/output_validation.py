
from utils.singleton_meta import SingletonMeta
from engine.utils.text import get_matching_words_in_text

blacklist_words = [
    "anthropic",
    "chatgpt",
    "gpt",
    "openai",
]

class OutputValidationHandler(metaclass=SingletonMeta):
    def get_errors(self,output:str):
        errors = []
        text_blacklist_words = get_matching_words_in_text(output,blacklist_words)
        if len(text_blacklist_words) > 0:
            err_string = "the following words are presented in the output text: " +",".join(text_blacklist_words)
            errors.append(err_string)
        return errors
    
    
    
