from langchain_core.language_models.chat_models import BaseChatModel
from services.prompt_templates import translation_prompt, translation_parser

class Translator:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.chain = translation_prompt | llm

    def translate(self, text_input: str):
        response = self.chain.invoke({"text_input": text_input})
        parsed_response = translation_parser.parse(response.content)
        return {
            "content": parsed_response["translated_text"],
            "metadata": {
                **response.response_metadata,
                "translation_status": parsed_response["status"]
            }
        }