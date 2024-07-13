from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

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