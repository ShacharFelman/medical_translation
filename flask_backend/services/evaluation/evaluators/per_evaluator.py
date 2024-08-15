from utils.logger import logger
from typing import List, Union
from jiwer import per

class PEREvaluator():
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

            total_per = 0.0
            for ref, hyp in zip(reference_sentences, hypothesis_sentences):
                per_score = per(reference=ref, hypothesis=hyp)
                total_per += per_score

            average_per = total_per / len(reference_sentences)
            return average_per

        except Exception as e:
            logger.error(f"An error occurred while calculating PER score: {str(e)}")
            return 0.0
        
    async def evaluate_async(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        return self.evaluate(reference_sentences, hypothesis_sentences, source_sentences)