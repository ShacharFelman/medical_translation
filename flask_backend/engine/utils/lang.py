from utils.constants import Language
from langdetect import detect

def detect_lang(text: str) -> Language:
    try:
        detected_lang = detect(text)
        return Language.from_str(detected_lang)
    except:
        return Language.UNKNOWN
