import os
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.logger import logger
from utils.singleton_meta import SingletonMeta
from utils.exceptions import InvalidUserInputError
from services.llm_securcoity.prompt_templates import PROMPT_INJECTION_TEMPLATE

class InputValidator(metaclass=SingletonMeta):
    def __init__(self):
        self.threshold = 0.5
        self.model_name = 'gpt-4o'
        api_key_openai = os.getenv('API_KEY_OPENAI')
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0.0, api_key=api_key_openai)
        self.prompt = ChatPromptTemplate.from_template(PROMPT_INJECTION_TEMPLATE)
        self.chain = self.prompt | self.llm

    def validate_input(self, text_input: str) -> None:
        injection_score = self._check_prompt_injection(text_input)
        if injection_score > self.threshold:
            logger.warning(f"Potential prompt injection detected. Score: {injection_score}")
            raise InvalidUserInputError(
                english_message="Potential security risk detected in the input.",
                hebrew_message="זוהה סיכון אבטחה פוטנציאלי בקלט."
            )
        logger.info(f"Input validation passed. Injection score: {injection_score}")

    def _check_prompt_injection(self, user_input: str) -> float:
        try:
            result = self.chain.invoke({"user_input": user_input})
            return float(result.content.strip())
        except Exception as e:
            logger.error(f"Error in prompt injection detection: {str(e)}")
            return 1.0  # Assume it's an injection if there's an error
