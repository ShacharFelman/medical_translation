import os
from typing import Dict, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.logger import logger
from utils.singleton_meta import SingletonMeta
from services.llm_security.prompt_templates import PROMPT_INJECTION_TEMPLATE

class PromptInjectionDetector(metaclass=SingletonMeta):
    def __init__(self):
        self.threshold = 0.5
        self.model_name = 'gpt-4o'
        api_key_openai = os.getenv('API_KEY_OPENAI')
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0.0, api_key=api_key_openai)
        self.prompt = ChatPromptTemplate.from_template(PROMPT_INJECTION_TEMPLATE)
        self.chain = self.prompt | self.llm

    def validate_input(self, text_input: str) -> Tuple[bool, str]:
        injection_score = self._check_prompt_injection(text_input)
        if injection_score > self.threshold:
            logger.warning(f"Potential prompt injection detected. Score: {injection_score}")
            return False, f"Potential security risk detected in the input. Injection score: {injection_score}"
        logger.info(f"Input validation passed. Injection score: {injection_score}")
        return True, ""

    def _check_prompt_injection(self, user_input: str) -> float:
        try:
            result = self.chain.invoke({"user_input": user_input})
            return float(result.content.strip())
        except Exception as e:
            logger.error(f"Error in prompt injection detection: {str(e)}")
            return 1.0  # Assume it's an injection if there's an error