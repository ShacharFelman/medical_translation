from typing import Dict, Any
from utils.logger import logger
from langchain_core.language_models.chat_models import BaseChatModel
from services.translation.prompt_templates import translation_prompt, translation_parser
from data.boundaries import TranslatorLLMResponse


class TranslatorLLM:
    def __init__(self, llm: BaseChatModel, translator_name: str) -> None:
        self.llm = llm
        self.translator_name = translator_name
        self.chain = translation_prompt | llm

    def translate(self, text_input: str) -> TranslatorLLMResponse:
        try:
            if not self._is_valid_input(text_input):
                return self._create_error_response("Invalid or empty input", {})

            response = self.chain.invoke({"text_input": text_input})
            processed_response = self._handle_response(response)
            return processed_response

        except Exception as e:
            logger.exception(f"{self.translator_name}: An unexpected error occurred during translation: {str(e)}")
            return self._create_error_response(f"Unexpected error: {str(e)}", {})


    async def translate_async(self, text_input: str) -> TranslatorLLMResponse:
        try:
            if not self._is_valid_input(text_input):
                return self._create_error_response("Invalid or empty input", {})

            response = await self.chain.ainvoke({"text_input": text_input})
            
            processed_response = self._handle_response(response)
            return processed_response

        except Exception as e:
            logger.exception(f"{self.translator_name}: An unexpected error occurred during translation: {str(e)}")
            return self._create_error_response(f"Unexpected error: {str(e)}", {})


    def _is_valid_input(self, text_input: str) -> bool:
        if not isinstance(text_input, str) or not text_input.strip():
            logger.warning(f"{self.translator_name}: Invalid or empty input provided for translation.")
            return False
        
        return True


    def _handle_response(self, response):
        metadata = {}

        if hasattr(response, 'response_metadata'):
            metadata = response.response_metadata

        if not response or not hasattr(response, 'content'):
            logger.error(f"{self.translator_name}: Unexpected response format from language model.")
            return self._create_error_response("Unexpected response format", metadata)

        try:
            parsed_response = translation_parser.parse(response.content)
        except Exception as parse_error:
            logger.error(f"{self.translator_name}: Error parsing translation response: {str(parse_error)}")
            return self._create_error_response(f"Parsing error: {str(parse_error)}", metadata)

        if parsed_response.get("status") != "[TRANSLATION SUCCESSFUL]":
            logger.warning(f"{self.translator_name}: Translation not successful. Status: {parsed_response.get('status')}")
            return self._create_error_response(f"Translation not successful, status: {parsed_response.get('status')}, content: {parsed_response.get('translated_text', '')}", metadata)

        translated_text = parsed_response.get("translated_text", "").strip()
        if not translated_text:
            logger.warning(f"{self.translator_name}: Empty translation result.")
            return self._create_error_response("Empty translation result", metadata)

        return TranslatorLLMResponse(
            translator_name=self.translator_name,
            status="success",
            translated_text=translated_text,
            metadata=metadata
            )


    def _create_error_response(self, error_message: str, metadata: Dict[str, Any]) -> TranslatorLLMResponse:
        error_metadata = {
            **metadata,
            "error_message": error_message
        }
        
        return TranslatorLLMResponse(
            translator_name=self.translator_name,
            status="error",
            translated_text="",
            metadata=error_metadata
        )