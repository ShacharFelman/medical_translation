# from utils.logger import logger
# from data.entities import TranslationRecordEntity, TranslationEntity, EvaluationScores
# from services.evaluation.evaluators.comet_evaluator import COMETEvaluator
# from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
# from services.evaluation.evaluators.wer_evaluator import WEREvaluator
# from services.evaluation.evaluators.chrf_evaluator import CHRFEvaluator
# # from services.evaluation.evaluators.per_evaluator import PEREvaluator
# # from services.evaluation.evaluators.ter_evaluator import TEREvaluator


# class EvaluationManager():
#     def __init__(self):
#         self._initialized = False
#         self.comet_evaluator = COMETEvaluator()
#         self.bleu_evaluator = BLEUEvaluator
#         self.wer_evaluator = WEREvaluator()
#         self.chrf_evaluator = CHRFEvaluator()
#         # self.per_evaluator = PEREvaluator()
#         # self.ter_evaluator = TEREvaluator()

#     def evaluate(self, translation: TranslationEntity, bleu_type: str = None) -> EvaluationScores:
#         if not self._initialized:
#             raise RuntimeError("EvaluationManager is not initialized")

#         scores = EvaluationScores()

#         return scores
    
#     def _update_bleu_score(self, evaluation_scores: EvaluationScores,
#                           translated_text: str,
#                           human_translation: str,
#                           evaluation_type: str = "bleu_plain_corpus"):
#         score_updated = False
#         try:
#             logger.debug(f"Calculating BLEU score using {evaluation_type}")
#             bleu_score = self.bleu_evaluator.evaluate(
#                 reference_sentences= human_translation,
#                 hypothesis_sentences= translated_text,
#                 evaluation_type= evaluation_type
#                 )
            
#             if bleu_score and bleu_score > 0.0:
#                 logger.debug(f"Updating BLEU score using {evaluation_type}")
#                 if evaluation_type == "bleu_plain_corpus":
#                     evaluation_scores.bleu_plain_corpus = bleu_score
#                 elif evaluation_type == "bleu_token_corpus":
#                     evaluation_scores.bleu_token_corpus = bleu_score
#                 elif evaluation_type == "bleu_token_meth1":
#                     evaluation_scores.bleu_token_meth1 = bleu_score
#                 elif evaluation_type == "bleu_token_meth7":
#                     evaluation_scores.bleu_token_meth7 = bleu_score
#                 elif evaluation_type == "bleu_token_meth1_w":
#                     evaluation_scores.bleu_token_meth1_w = bleu_score
#                 elif evaluation_type == "bleu_token_meth7_w":
#                     evaluation_scores.bleu_token_meth7_w = bleu_score
#                 else:
#                     logger.warning(f"Unknown evaluation type: {evaluation_type}")
                    
#                 score_updated = True
#             else:
#                 logger.info(f"BLEU score is 0.0")

#             return score_updated, evaluation_scores
        
#         except Exception as e:
#             logger.error(f"Error calculating BLEU score: {str(e)}")
#             return score_updated, evaluation_scores


#     def update_comet_score(evaluation_scores: EvaluationScores, input: str, translated_text: str, human_translation: str):
#         score_updated = False
#         try:
#             logger.info(f"Calculating COMET score")
#             comet_score = comet_evaluator.evaluate(
#                 reference_sentences=[human_translation],
#                 hypothesis_sentences=[translated_text],
#                 source_sentences=[input]
#                 )
            
#             if comet_score and comet_score > 0.0:
#                 logger.info(f"Updating COMET score")
#                 evaluation_scores.comet_score = comet_score
#                 score_updated = True
#             else:
#                 logger.info(f"COMET score is 0.0")
            
#             return score_updated, evaluation_scores
        
#         except Exception as e:
#             logger.error(f"Error calculating COMET score: {str(e)}")
#             return score_updated, evaluation_scores


#     def update_chrf_score(evaluation_scores: EvaluationScores, translated_text: str, human_translation: str):
#         score_updated = False
#         try:
#             logger.info(f"Calculating chrF score")
#             chrf_score = chrf_evaluator.evaluate(
#                 reference_sentences=[human_translation],
#                 hypothesis_sentences=[translated_text]
#                 )
            
#             if chrf_score and chrf_score > 0.0:
#                 logger.info(f"Updating chrF score")
#                 evaluation_scores.chrf_score = chrf_score
#                 score_updated = True
#             else:
#                 logger.info(f"chrF score is 0.0")

#             return score_updated, evaluation_scores
        
#         except Exception as e:
#             logger.error(f"Error calculating chrF score: {str(e)}")
#             return score_updated, evaluation_scores


#     def update_wer_score(evaluation_scores: EvaluationScores, translated_text: str, human_translation: str):
#         score_updated = False
#         try:
#             logger.info(f"Calculating wer score")
#             wer_score = wer_evaluator.evaluate(
#                 reference_sentences=[human_translation],
#                 hypothesis_sentences=[translated_text]
#                 )

#             if wer_score and wer_score > 0.0:
#                 logger.info(f"Updating wer score")
#                 evaluation_scores.wer_score = wer_score
#                 score_updated = True
#             else:
#                 logger.info(f"wer score is 0.0")
            
#             return score_updated, evaluation_scores
        
#         except Exception as e:
#             logger.error(f"Error calculating wer score: {str(e)}")
#             return score_updated, evaluation_scores