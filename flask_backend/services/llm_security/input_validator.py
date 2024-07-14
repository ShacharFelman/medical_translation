from services.llm_security.prompt_injection_detector import PromptInjectionDetector
from utils.logger import logger
from utils.exceptions import InvalidUserInputError

class InputValidator:
    def __init__(self):
        self.prompt_injection_detector = PromptInjectionDetector()

    def validate_input(self, text_input: str) -> None:
        injection_score = self.prompt_injection_detector.check_prompt_injection(text_input)
        if self.prompt_injection_detector.is_prompt_injection_detected(injection_score):
            logger.warning(f"Potential prompt injection detected. Score: {injection_score}")
            raise InvalidUserInputError(
                english_message="Potential security risk detected in the input.",
                hebrew_message="זוהה סיכון אבטחה פוטנציאלי בקלט."
            )
        logger.info(f"Input validation passed. Injection score: {injection_score}")