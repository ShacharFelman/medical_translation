from utils.logger import logger
from sacrebleu.metrics import CHRF

class CHRFEvaluator():
    def __init__(self):
        self.chrf = CHRF()

    def evaluate(self,
                 reference: str, 
                 candidate: str
                 ) -> float:
        try:
            reference, candidate = self._preprocess_input(reference, candidate)

            if not reference or not candidate:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            total_chrf = 0.0
            for ref, cand in zip(reference, candidate):
                chrf_score = self.chrf.sentence_score(hypothesis=cand, references=[ref]).score
                total_chrf += chrf_score

            average_chrf = total_chrf / len(reference)
            return average_chrf / 100
        except Exception as e:
            logger.error(f"An error occurred while calculating CHRF score: {str(e)}")
            return 0.0
        
    async def evaluate_async(self,
                             reference: str, 
                             candidate: str
                             ) -> float:
        return self.evaluate(reference, candidate)
    

    def _preprocess_input(self, reference: str, candidate: str):
        ref, cand = reference.lower(), candidate.lower()
        ref     = [reference]
        cand    = [candidate]
        return ref, cand