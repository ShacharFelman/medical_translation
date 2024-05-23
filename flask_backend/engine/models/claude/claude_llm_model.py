import anthropic
from exceptions import InvalidUserInputError
from typing import List
from logger import logger
import json

class ClaudeLLMModel():
    '''
    Base class containing general usage Claude functions for the other Claude models.
    '''
    def __init__(self, model_name: str, api_key: str,max_tokens_limit: int) -> None:
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=api_key)
        self.max_tokens_limit = max_tokens_limit

    def send_claude_prompt(self, system_message: str, text_prompt: str, stop_sequences: List[str] | None):
        messages = [{"role": "user", "content": text_prompt}]
        
        params = {
            'model': self.model_name,
            'max_tokens': self.max_tokens_limit,
            'temperature': 0.0,
            'system': system_message,
            'messages': messages
        }

        if stop_sequences is not None:
            params['stop_sequences'] = stop_sequences

        response = self.client.messages.create(**params)

        return response

    def is_valid_string_input(self, text_input:str):
        if not text_input:
            return False
        if text_input.isspace():
            return False

        return True

    def count_tokens(self, text: str) -> int:
        '''
        Since Anthropic does not a tokenizer available for Claude 3, we will have to broadly estimate the amount of tokens used.

        Since Hebrew uses around ~0.85 tokens per character, as of right now we will simply count the characters in the text.
        '''
        return len(text)