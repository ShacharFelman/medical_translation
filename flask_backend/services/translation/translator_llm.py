from utils.logger import logger
from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel
from services.translation.prompt_templates import translation_prompt, translation_parser

class TranslatorLLM:
    def __init__(self, llm: BaseChatModel, model_name: str) -> None:
        self.llm = llm
        self.model_name = model_name
        self.chain = translation_prompt | llm

    def translate(self, text_input: str) -> Dict[str, Any]:
        try:
            if not isinstance(text_input, str) or not text_input.strip():
                logger.warning("Invalid or empty input provided for translation.")
                return self._create_error_response("Invalid input")

            response = self.chain.invoke({"text_input": text_input})
            
            if not response or not hasattr(response, 'content'):
                logger.error("Unexpected response format from language model.")
                return self._create_error_response("Unexpected response format")

                #hasdfkjhsadkfjhasdkfjhsadkfjhsadkfj

            try:
                parsed_response = translation_parser.parse(response.content)
            except Exception as parse_error:
                logger.error(f"Error parsing translation response: {str(parse_error)}")
                return self._create_error_response("Parsing error")

            return {
                "model_name": self.model_name,
                "status": parsed_response.get("status", "unknown"),
                "content": parsed_response.get("translated_text", ""),
                "metadata": {
                    **(response.response_metadata if hasattr(response, 'response_metadata') else {})
                }
            }

        except Exception as e:
            logger.exception(f"An unexpected error occurred during translation: {str(e)}")
            return self._create_error_response("Unexpected error")

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        return {
            "content": "",
            "metadata": {
                "translation_status": "error",
                "error_message": error_message
            }
        }