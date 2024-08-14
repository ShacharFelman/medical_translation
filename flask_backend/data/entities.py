import uuid
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class EvaluationScores(BaseModel):
    bleu_score: Optional[float] = None
    bleu_plain_corpus: Optional[float] = None
    bleu_token_corpus: Optional[float] = None
    bleu_token_meth1: Optional[float] = None
    bleu_token_meth7: Optional[float] = None
    bleu_token_meth1_w: Optional[float] = None
    bleu_token_meth7_w: Optional[float] = None
    comet_score: Optional[float] = None
    ter_score: Optional[float] = None
    chrf_score: Optional[float] = None
    per_score: Optional[float] = None
    wer_score: Optional[float] = None

class TranslationEntity(BaseModel):
    translator_name: str
    translated_text: str
    response_time: float
    score: Optional[float] = None
    evaluation_scores: Optional[EvaluationScores] = None
    metadata: Dict[str, Any] = {}

    def __repr__(self):
        return f"TranslationEntity(translator_name='{self.translator_name}', translated_text='{self.translated_text[:50]}...', response_time={self.response_time}, score={self.score}, evaluation_scores={self.evaluation_scores})"


class EvaluationLeafletData(BaseModel):
    leaflet_id: Optional[int] = None
    leaflet_name: Optional[str] = None
    section_number: Optional[int] = None
    array_location: Optional[int] = None
    human_translation: Optional[str] = None


class TranslationRecordEntity(BaseModel):
    input: str
    translations: List[TranslationEntity]
    best_translation: Optional[TranslationEntity] = None
    timestamp: datetime = datetime.now()
    evaluation_leaflet_data: Optional[EvaluationLeafletData] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranslationRecordEntity':
        return cls(**data)
    

class LeafletSectionEntity(BaseModel):
    id: int
    input_text: str
    translated_text: str


class LeafletHistoryEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    date: datetime = Field(default_factory=datetime.now)
    sections: List[LeafletSectionEntity]

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeafletHistoryEntity':
        data.pop('_id', None)
        sections = [LeafletSectionEntity(**section) for section in data.get('sections', [])]
        return cls(**{**data, 'sections': sections})