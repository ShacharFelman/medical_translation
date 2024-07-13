from pydantic import BaseModel
from typing import Dict, Any

class TranslatorLLMResponse(BaseModel):
    translator_name: str
    status: str
    translated_text: str
    metadata: Dict[str, Any] = {}

class TranslationRequest(BaseModel):
    source: str
    dest: str
    text_input: str

class TranslationResponse(BaseModel):
    translated_text: str
    translator_used: str
    confidence_score: float