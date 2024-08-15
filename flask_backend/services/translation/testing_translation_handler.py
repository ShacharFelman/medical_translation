from utils.logger import logger
from services.translation.base_translation_handler import BaseTranslationHandler
from services.evaluation.evaluation_manager import EvaluationManager
from data.entities import TranslationEntity, EvaluationLeafletData


class TestingTranslationHandler(BaseTranslationHandler):
    def __init__(self):
        super().__init__()
        self.evalution_manager = EvaluationManager()


    def _process_translation(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        evaluation_leaflet_data: EvaluationLeafletData = kwargs.get('evaluation_leaflet_data')
        evaluate: bool = kwargs.get('evaluate', False)

        translation_updated = translation

        if evaluation_leaflet_data and self._is_translation_successful(translation) and evaluate:
            scores_updated, translation_updated = self.evalution_manager.update_translation_scores(translation, evaluation_leaflet_data.human_translation, text_input)
            if not scores_updated:
                logger.error("Failed to update translation scores.")

        return translation_updated


    async def _process_translation_async(self, translation: TranslationEntity, text_input: str, **kwargs) -> TranslationEntity:
        return self._process_translation(translation, text_input, **kwargs)


    @staticmethod
    def _is_translation_successful(translation: TranslationEntity) -> bool:
        return (
            translation.metadata.get('status') != 'error' and
            translation.translated_text and
            translation.translated_text.strip() != ""
        )
