from services.evaluation.evaluator import EvaluationStrategy
from utils.logger import logger
from typing import List, Union
from sacrebleu.metrics import CHRF

class CHRFEvaluator(EvaluationStrategy):
    def __init__(self):
        self.chrf = CHRF()

    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        try:
            if isinstance(reference_sentences, str):
                reference_sentences = [reference_sentences]
            if isinstance(hypothesis_sentences, str):
                hypothesis_sentences = [hypothesis_sentences]

            if not reference_sentences or not hypothesis_sentences:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            if len(reference_sentences) != len(hypothesis_sentences):
                logger.warning("Mismatch in number of reference and hypothesis sentences.")
                return 0.0

            total_chrf = 0.0
            for ref, hyp in zip(reference_sentences, hypothesis_sentences):
                chrf_score = self.chrf.sentence_score(hypothesis=hyp, references=[ref]).score
                total_chrf += chrf_score

            average_chrf = total_chrf / len(reference_sentences)
            return average_chrf / 100  # Normalize to 0-1 range

        except Exception as e:
            logger.error(f"An error occurred while calculating CHRF score: {str(e)}")
            return 0.0
        
    async def evaluate_async(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        return self.evaluate(reference_sentences, hypothesis_sentences, source_sentences)