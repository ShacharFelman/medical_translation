from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class TranslatorLLMResponse(BaseModel):
    translator_name: str
    status: str
    translated_text: str
    metadata: Dict[str, Any] = {}

class TranslationRequest(BaseModel):
    source: str
    dest: str
    textInput: str

class TranslationResponse(BaseModel):
    translated_text: str
    translator_used: str

class LeafletSectionInput(BaseModel):
    id: int
    inputText: str
    translation: str

class LeafletSaveRequest(BaseModel):
    name: str
    sections: List[LeafletSectionInput]

class LeafletResponse(BaseModel):
    id: str
    name: str
    date: datetime
    sections: List[LeafletSectionInput]

class FetchLeafletsResponse(BaseModel):
    leaflets: List[LeafletResponse]

class TranslationDownloadRequest(BaseModel):
    input: str

    