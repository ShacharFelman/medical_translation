from typing import Dict, Tuple, Any, List, Union
from utils.logger import logger
from data.entities import TranslationRecordEntity, TranslationEntity, EvaluationScores
from utils.constants import EvaluationScoreType, BLEUScoreType
from services.evaluation.evaluators.comet_evaluator import COMETEvaluator
from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from services.evaluation.evaluators.wer_evaluator import WEREvaluator
from services.evaluation.evaluators.chrf_evaluator import CHRFEvaluator
# from services.evaluation.evaluators.per_evaluator import PEREvaluator
# from services.evaluation.evaluators.ter_evaluator import TEREvaluator


class EvaluationManager():
    def __init__(self):
        self.comet_evaluator    = COMETEvaluator()
        self.bleu_evaluator     = BLEUEvaluator
        self.wer_evaluator      = WEREvaluator()
        self.chrf_evaluator     = CHRFEvaluator()
        # self.per_evaluator    = PEREvaluator()
        # self.ter_evaluator    = TEREvaluator()


    def update_translation_entity_scores(self,
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
                                  source: str,
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
                      source: str,
                      score_types: Union[str, List[str]] = None,
                      bleu_types: Union[str, List[str]] = None
                      ) -> Tuple[bool, Dict[str, Any]]:
        scores_updated = False
        evaluation_scores = {} if evaluation_scores is None else evaluation_scores
        score_types = [score_types] if isinstance(bleu_types, str) else bleu_types
        types = score_types if score_types and len(bleu_types) > 0 else EvaluationScoreType.get_types()
        for score_type in types:
            if score_type in EvaluationScoreType.get_types():
                updated, new_scores = self._update_score(score_type, reference, candidate, source, bleu_types)
                if updated:
                    evaluation_scores.update(new_scores)
                    scores_updated = True
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
            if score_type == EvaluationScoreType.BLEU.value:
                return self._update_bleu_score(reference, candidate, bleu_types=bleu_types)

            elif score_type == EvaluationScoreType.COMET.value:
                score = self.comet_evaluator.evaluate(reference, candidate, source)
                return score is not None and score > 0.0, {EvaluationScoreType.COMET.value: score}

            elif score_type == EvaluationScoreType.CHRF.value:
                score = self.chrf_evaluator.evaluate([reference], [candidate])
                return score is not None and score > 0.0, {EvaluationScoreType.CHRF.value: score}

            elif score_type == EvaluationScoreType.WER.value:
                score = self.wer_evaluator.evaluate([reference], [candidate])
                return score is not None and score > 0.0, {EvaluationScoreType.WER.value: score}

            else:
                logger.warning(f"Unknown score type: {score_type}")
                return False, {}

        except Exception as e:
            logger.error(f"Error calculating {score_type} score: {str(e)}")
            return False, {}
        

    def _update_bleu_score(self, reference: str, candidate: str, bleu_types: Union[str, List[str]] = None) -> Tuple[bool, Dict[str, Any]]:
        try:
            bleu_types = [bleu_types] if isinstance(bleu_types, str) else bleu_types
            types = bleu_types if bleu_types and len(bleu_types) > 0 else BLEUScoreType.get_types()
            bleu_scores = {}
            for bleu_type in types:
                if bleu_type in BLEUScoreType.get_types():
                    score = self.bleu_evaluator.evaluate(reference, candidate, evaluation_type=bleu_type)
                    if score is not None and score > 0.0:
                        bleu_scores[bleu_type] = score
                else:
                    logger.warning(f"Unknown BLEU score type: {bleu_type}")
            return len(bleu_scores) > 0, {EvaluationScoreType.BLEU.value: bleu_scores}

        except Exception as e:
            logger.error(f"Error calculating BLEU score: {str(e)}")
            return False, {}

    # def update_comet_score(evaluation_scores: EvaluationScores, input: str, translated_text: str, human_translation: str):
    #     score_updated = False
    #     try:
    #         logger.info(f"Calculating COMET score")
    #         comet_score = comet_evaluator.evaluate(
    #             reference_sentences=[human_translation],
    #             hypothesis_sentences=[translated_text],
    #             source_sentences=[input]
    #             )
            
    #         if comet_score and comet_score > 0.0:
    #             logger.info(f"Updating COMET score")
    #             evaluation_scores.comet_score = comet_score
    #             score_updated = True
    #         else:
    #             logger.info(f"COMET score is 0.0")
            
    #         return score_updated, evaluation_scores
        
    #     except Exception as e:
    #         logger.error(f"Error calculating COMET score: {str(e)}")
    #         return score_updated, evaluation_scores


    # def update_chrf_score(evaluation_scores: EvaluationScores, translated_text: str, human_translation: str):
    #     score_updated = False
    #     try:
    #         logger.info(f"Calculating chrF score")
    #         chrf_score = chrf_evaluator.evaluate(
    #             reference_sentences=[human_translation],
    #             hypothesis_sentences=[translated_text]
    #             )
            
    #         if chrf_score and chrf_score > 0.0:
    #             logger.info(f"Updating chrF score")
    #             evaluation_scores.chrf_score = chrf_score
    #             score_updated = True
    #         else:
    #             logger.info(f"chrF score is 0.0")

    #         return score_updated, evaluation_scores
        
    #     except Exception as e:
    #         logger.error(f"Error calculating chrF score: {str(e)}")
    #         return score_updated, evaluation_scores


    # def update_wer_score(evaluation_scores: EvaluationScores, translated_text: str, human_translation: str):
    #     score_updated = False
    #     try:
    #         logger.info(f"Calculating wer score")
    #         wer_score = wer_evaluator.evaluate(
    #             reference_sentences=[human_translation],
    #             hypothesis_sentences=[translated_text]
    #             )

    #         if wer_score and wer_score > 0.0:
    #             logger.info(f"Updating wer score")
    #             evaluation_scores.wer_score = wer_score
    #             score_updated = True
    #         else:
    #             logger.info(f"wer score is 0.0")
            
    #         return score_updated, evaluation_scores
        
    #     except Exception as e:
    #         logger.error(f"Error calculating wer score: {str(e)}")
    #         return score_updated, evaluation_scores