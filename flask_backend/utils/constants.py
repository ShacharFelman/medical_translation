from enum import Enum
from typing import List, Optional

class EvaluationScoreType(Enum):
    BLEU    = 'bleu'
    # COMET   = 'comet'
    CHRF    = 'chrf'
    WER     = 'wer'

    @classmethod
    def get_types(cls) -> List[str]:
        return [score_type.value for score_type in EvaluationScoreType]

class BLEUScoreType(Enum):
    PLAIN_CORPUS                = 'plain_corpus'
    TOKENIZED_CORPUS            = 'tokenized_corpus'
    TOKENIZED_METHOD1           = 'tokenized_method1'
    TOKENIZED_METHOD1_WEIGHTS   = 'tokenized_method1_weights'

    @classmethod
    def get_types(cls) -> List[str]:
        return [score_type.value for score_type in BLEUScoreType]

    @classmethod
    def get_types_tokenized(cls) -> List[str]:
        types = [score_type.value for score_type in BLEUScoreType]
        types.remove(BLEUScoreType.PLAIN_CORPUS.value)
        return types

EVALUATION_SCORE_TYPES = [score_type.value for score_type in BLEUScoreType]


# TODO: Check if needed
class Language(Enum):
    HE = 'heb'
    EN = 'eng'
    ARAB = 'ara'
    ENGLISH = 'en'
    HEBREW = 'he'
    ARABIC = 'ar'
    UNKNOWN = 'unknown'

    @classmethod
    def from_str(cls,lang_name: str):
        if lang_name.lower() in ('en', 'eng', 'english'):
            return Language.ENGLISH
        if lang_name.lower() in ('he', 'heb', 'hebrew'):
            return Language.HEBREW
        if lang_name.lower() in ('ar', 'ara', 'arabic'):
            return Language.ARABIC
        
# TODO: Check if needed
class FileType(Enum):
    PDF = 'pdf'
    DOC = 'doc'
    DOCX = 'docx'
    TXT = 'txt'

    @classmethod
    def get_file_type(cls, filename: str) -> Optional["FileType"]:
        file_extension = filename.split('.')[-1].lower()
        for file_type in cls:
            if file_extension == file_type.value:
                return file_type
