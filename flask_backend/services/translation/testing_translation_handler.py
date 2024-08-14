import time
from typing import List
from utils.logger import logger
from services.translation.base_translation_handler import BaseTranslationHandler
from services.evaluation.evaluators.comet_evaluator import COMETEvaluator
from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from data.entities import TranslationEntity, EvaluationScores, EvaluationLeafletData


class TestingTranslationHandler(BaseTranslationHandler):
    def __init__(self):
        super().__init__()
        self.comet_evaluator = COMETEvaluator()
        self.bleu_evaluator = BLEUEvaluator()


    def _process_translation(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        evaluation_leaflet_data: EvaluationLeafletData = kwargs.get('evaluation_leaflet_data')

        if evaluation_leaflet_data and self._is_translation_successful(translation):
            bleu_score = self.bleu_evaluator.evaluate(evaluation_leaflet_data.human_translation, translation.translated_text)
            # comet_score = self.comet_evaluator.evaluate([evaluation_leaflet_data.human_translation], [translation.translated_text], [text_input])
          
            translation.evaluation_scores = EvaluationScores(bleu_score=bleu_score)
        return translation


    async def _process_translation_async(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        evaluation_leaflet_data: EvaluationLeafletData = kwargs.get('evaluation_leaflet_data')

        if evaluation_leaflet_data and self._is_translation_successful(translation):
            bleu_score = await self.bleu_evaluator.evaluate_async(evaluation_leaflet_data.human_translation, translation.translated_text)
            # comet_score = await self.comet_evaluator.evaluate_async([evaluation_leaflet_data.human_translation], [translation.translated_text], [text_input])
          
            translation.evaluation_scores = EvaluationScores(bleu_score=bleu_score)
        return translation


    @staticmethod
    def _is_translation_successful(translation: TranslationEntity) -> bool:
        return (
            translation.metadata.get('status') != 'error' and
            translation.translated_text and
            translation.translated_text.strip() != ""
        )
