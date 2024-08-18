from typing import Dict, Tuple, Any, List, Union
from utils.logger import logger
from data.entities import TranslationRecordEntity, TranslationEntity
from utils.constants import EvaluationScoreType, BLEUScoreType
from services.evaluation.evaluators.comet_evaluator import COMETEvaluator
from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from services.evaluation.evaluators.wer_evaluator import WEREvaluator
from services.evaluation.evaluators.chrf_evaluator import CHRFEvaluator
# from services.evaluation.evaluators.per_evaluator import PEREvaluator
# from services.evaluation.evaluators.ter_evaluator import TEREvaluator


class EvaluationManager():
    def __init__(self):
        self._comet_evaluator    = COMETEvaluator()
        self._bleu_evaluator     = BLEUEvaluator()
        self._wer_evaluator      = WEREvaluator()
        self._chrf_evaluator     = CHRFEvaluator()
        # self.per_evaluator    = PEREvaluator()
        # self.ter_evaluator    = TEREvaluator()


    def update_record_scores(self,
                                         record: TranslationRecordEntity,
                                         score_types: Union[str, List[str]] = None,
                                         bleu_types: Union[str, List[str]] = None
                                         ) -> Tuple[bool, TranslationEntity]:
        scores_updated = False
        reference = record.evaluation_leaflet_data.human_translation
        source = record.input,
        for translation in record:
            update, translation = self.update_translation_scores(translation,
                                                                 reference,
                                                                 source,
                                                                 score_types,
                                                                 bleu_types)
            if update:
                scores_updated = True
                if (record.best_translation and 
                    record.best_translation.translator_name == translation.translator_name):
                    record.best_translation = translation

        return scores_updated, record


    def update_translation_scores(self,
                                  translation: TranslationEntity,
                                  reference: str,
                                  source: str = None,
                                  score_types: Union[str, List[str]] = None,
                                  bleu_types: Union[str, List[str]] = None
                                  ) -> Tuple[bool, TranslationEntity]:
        scores_updated, translation.evaluation_scores = self.update_scores(translation.evaluation_scores,
                                                                           reference,
                                                                           translation.translated_text,
                                                                           source,
                                                                           score_types,
                                                                           bleu_types)
        return scores_updated, translation


    def update_scores(self,
                      evaluation_scores: Dict[str, float],
                      reference: str,
                      candidate: str,
                      source: str = None,
                      score_types: Union[str, List[str]] = None,
                      bleu_types: Union[str, List[str]] = None
                      ) -> Tuple[bool, Dict[str, Any]]:
        scores_updated = False
        evaluation_scores = {} if evaluation_scores is None else evaluation_scores
        score_types = [score_types] if isinstance(score_types, str) else score_types
        types = score_types if score_types and len(score_types) > 0 else EvaluationScoreType.get_types()
        for score_type in types:
            if score_type in EvaluationScoreType.get_types():
                updated, new_scores = self._update_score(reference, candidate, score_type, source, bleu_types)
                if updated:
                    evaluation_scores.update(new_scores)
                    scores_updated = True
                else:
                    logger.warning(f"Failed to update {score_type} score")
            else:
                logger.warning(f"Unknown score type: {score_type}")

        return scores_updated, evaluation_scores


    def _update_score(self,
                    reference: str,
                    candidate: str,
                    score_type: str,
                    source: str = None,
                    bleu_types: Union[str, List[str]] = None
                    ) -> Tuple[bool, Dict[str, Any]]:
        try:
            logger.info(f"Updating {score_type} score")
            if score_type == EvaluationScoreType.BLEU.value:
                return self._update_bleu_score(reference, candidate, bleu_types)

            elif score_type == EvaluationScoreType.COMET.value:
                return self._update_comet_score(reference, candidate, source)

            elif score_type == EvaluationScoreType.CHRF.value:
                score = self._chrf_evaluator.evaluate(reference, candidate)
                return score is not None and score > 0.0, {EvaluationScoreType.CHRF.value: score}

            elif score_type == EvaluationScoreType.WER.value:
                score = self._wer_evaluator.evaluate(reference, candidate)
                return score is not None and score > 0.0, {EvaluationScoreType.WER.value: score}

            else:
                logger.warning(f"Unknown score type: {score_type}")
                return False, {}

        except Exception as e:
            logger.error(f"Error calculating {score_type} score: {str(e)}")
            return False, {}
        

    def _update_bleu_score(self, reference: str, candidate: str, bleu_types: Union[str, List[str]] = None) -> Tuple[bool, Dict[str, Any]]:
        try:
            if bleu_types:
                bleu_types = [bleu_types] if isinstance(bleu_types, str) else bleu_types
              
            types = bleu_types if bleu_types and len(bleu_types) > 0 else BLEUScoreType.get_types()
            bleu_scores = {}
            for bleu_type in types:
                logger.info(f"Updating {bleu_type} score")
                if bleu_type in BLEUScoreType.get_types():
                    score = self._bleu_evaluator.evaluate(reference, candidate, bleu_type)
                if score is not None and score > 0.0:
                    bleu_scores[bleu_type] = score
                else:
                    logger.warning(f"Unknown BLEU score type: {bleu_type}")
            return len(bleu_scores) > 0, {EvaluationScoreType.BLEU.value: bleu_scores}

        except Exception as e:
            logger.error(f"Error calculating BLEU score: {str(e)}")
            return False, {}
        

    def _update_comet_score(self, reference: str, candidate: str, source: str) -> Tuple[bool, Dict[str, Any]]:
        try:
            if source:
                score = self._comet_evaluator.evaluate(reference, candidate, source)
                return score is not None and score > 0.0, {EvaluationScoreType.COMET.value: score}
            else:
                logger.warning("COMET score requires source text")
                return False, {}
        except Exception as e:
            logger.error(f"Error calculating COMET score: {str(e)}")
            return False, {}
