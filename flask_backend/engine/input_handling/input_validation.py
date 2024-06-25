
from engine.utils.lang import detect_lang
from utils.constants import Language
from utils.exceptions import InvalidUserInputError
from utils.singleton_meta import SingletonMeta
from engine.models.model_config import model_config
from utils.logger import logger

class InputValidationHandler(metaclass=SingletonMeta):

    def get_errors(self,input:str):
        errors = []
        if not self._is_language_supported(input):
            errors.append("unsupported language")
        if self.is_over_token_limit(input):
            raise InvalidUserInputError("text is too long","טקסט גדול מידי")            
        return errors
        
    def is_over_token_limit(self,text_input): # TODO move 
        return len(text_input) > model_config.MAX_TOKENS_LIMIT
    
    def _is_language_supported(self,text_input):
        input_language = detect_lang(text_input)
        if input_language != Language.HEBREW:
            return False
        return True
    
    # if self.is_injection(text_input):
#     raise InvalidUserInputError("invalid prompt text","טקסט לא תקין")

    
