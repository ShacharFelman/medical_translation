from utils.logger import logger
from typing import List
from services.translation.base_translation_handler import BaseTranslationHandler
from services.evaluation.comet_evaluator import COMETEvaluator
from services.evaluation.bleu_evaluator import BLEUEvaluator
from data.entities import TranslationEntity, EvaluationScores


class TestingTranslationHandler(BaseTranslationHandler):
    def __init__(self):
        super().__init__()
        self.comet_evaluator = COMETEvaluator()
        self.bleu_evaluator = BLEUEvaluator()

    def translate(self, text_input: str, **kwargs) -> List[TranslationEntity]:
        translations = self.translate_text(text_input)
        evaluation_leaflet_data = kwargs.get('evaluation_leaflet_data')

        # Calculate BLEU and COMET scores for successful translations
        if evaluation_leaflet_data:
            for translation in translations:
                if self._is_translation_successful(translation):
                    bleu_score = self.bleu_evaluator.evaluate(evaluation_leaflet_data.human_translation, translation.translated_text)
                    comet_score = self.comet_evaluator.evaluate([evaluation_leaflet_data.human_translation], [translation.translated_text], [text_input])
                    translation.evaluation_scores = EvaluationScores(bleu_score=bleu_score, comet_score=comet_score)

        return translations

    @staticmethod
    def _is_translation_successful(translation: TranslationEntity) -> bool:
        return (
            translation.metadata.get('status') != 'error' and
            translation.translated_text and
            translation.translated_text.strip() != ""
        )
