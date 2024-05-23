from .claude_translation_model import ClaudeTranslationModel
from .claude_validation_model import ClaudeValidationModel
import os

api_key = os.getenv('ANTHROPIC_API_KEY')
claude_translation_model_instance = ClaudeTranslationModel(model_name="claude-3-opus-20240229", 
                                                           api_key=api_key,
                                                           max_tokens_limit=4096) #temporarily set at max TODO set at lower number

# claude_validation_model_instance = ClaudeValidationModel(model_name="claude-3-opus-20240229",
#                                                          api_key=api_key,
#                                                          max_tokens_limit=MAX_TOKENS_LIMIT)