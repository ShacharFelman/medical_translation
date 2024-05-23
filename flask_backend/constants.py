import enum
import typing

class Language(enum.Enum):
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
        

class FileType(enum.Enum):
    PDF = 'pdf'
    DOC = 'doc'
    DOCX = 'docx'
    TXT = 'txt'

    @classmethod
    def get_file_type(cls, filename: str) -> typing.Optional["FileType"]:
        file_extension = filename.split('.')[-1].lower()
        for file_type in cls:
            if file_extension == file_type.value:
                return file_type
