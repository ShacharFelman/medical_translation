from typing import List
from data.entities import TranslationEntity
from services.translation.base_translation_handler import BaseTranslationHandler


class RuntimeTranslationHandler(BaseTranslationHandler):
    def translate(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        return self.translate_text(text_input)
