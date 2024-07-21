import uuid

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId

class TranslationEntity(BaseModel):
    translator_name: str
    translated_text: str
    response_time: float
    score: Optional[float] = None
    bleu_score: Optional[float] = None
    metadata: Dict[str, Any] = {}

    def __repr__(self):
        return f"TranslationEntity(translator_name='{self.translator_name}', output='{self.output[:50]}...', response_time={self.response_time}, score={self.score}, bleu_score={self.bleu_score})"

class TranslationRecordEntity(BaseModel):
    input: str
    translations: List[TranslationEntity]
    best_translation: Optional[TranslationEntity] = None
    timestamp: datetime = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranslationRecordEntity':
        return cls(**data)
    
class LeafletSectionEntity(BaseModel):
    id: int
    # id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_text: str
    translated_text: str

class LeafletHistoryEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    date: datetime
    sections: List[LeafletSectionEntity]
    timestamp: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeafletHistoryEntity':
        # Ignore MongoDB's '_id' field if present
        data.pop('_id', None)
        sections = [LeafletSectionEntity(**section) for section in data.get('sections', [])]
        return cls(**{**data, 'sections': sections})