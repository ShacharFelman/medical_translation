from utils.logger import logger
from jiwer import wer

class WEREvaluator():
    def evaluate(self,
                 reference:str, 
                 candidate: str 
                 ) -> float:
        try:
            reference, candidate = self._preprocess_input(reference, candidate)
            
            if not reference or not candidate:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            total_wer = 0.0
            for ref, cand in zip(reference, candidate):
                wer_score = wer(reference=ref, hypothesis=cand)
                total_wer += wer_score

            average_wer = total_wer / len(ref)
            return average_wer

        except Exception as e:
            logger.error(f"An error occurred while calculating WER score: {str(e)}")
            return 0.0
        
    async def evaluate_async(self,
                             reference:str,
                             candidate: str
                             ) -> float:
        return self.evaluate(reference, candidate)
    

    def _preprocess_input(self, reference: str, candidate: str):
        ref, cand = reference.lower(), candidate.lower()
        ref     = [reference]
        cand    = [candidate]
        return ref, cand