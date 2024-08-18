from enum import Enum
from typing import List, Optional

class EvaluationScoreType(Enum):
    BLEU    = 'bleu'
    # COMET   = 'comet'
    CHRF    = 'chrf'
    WER     = 'wer'
    # TER     = 'ter'
    # PER     = 'per'

    @classmethod
    def get_types(cls) -> List[str]:
        return [score_type.value for score_type in EvaluationScoreType]

class BLEUScoreType(Enum):
    PLAIN_CORPUS                = 'plain_corpus'
    TOKENIZED_CORPUS            = 'tokenized_corpus'
    TOKENIZED_METHOD1           = 'tokenized_method1'
    TOKENIZED_METHOD1_WEIGHTS   = 'tokenized_method1_weights'
    # TOKENIZED_METHOD7           = 'tokenized_method7'
    # TOKENIZED_METHOD7_WEIGHTS   = 'tokenized_method7_weights'

    @classmethod
    def get_types(cls) -> List[str]:
        return [score_type.value for score_type in BLEUScoreType]

EVALUATION_SCORE_TYPES = [score_type.value for score_type in BLEUScoreType]


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
