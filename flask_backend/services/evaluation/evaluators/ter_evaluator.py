from utils.logger import logger
from typing import List, Union
# import pyter

class TEREvaluator():
    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        try:
            reference_sentences = [reference_sentences] if isinstance(reference_sentences, str) else reference_sentences
            hypothesis_sentences = [hypothesis_sentences] if isinstance(hypothesis_sentences, str) else hypothesis_sentences

            if not reference_sentences or not hypothesis_sentences:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            total_ter = 0.0
            count = 0

            for ref, hyp in zip(reference_sentences, hypothesis_sentences):
                ref_tokens = ref.split()
                hyp_tokens = hyp.split()
                # ter_score = pyter.ter(hyp_tokens, ref_tokens)
                # total_ter += ter_score
                count += 1

            average_ter = total_ter / count if count > 0 else 0.0
            return average_ter

        except Exception as e:
            logger.error(f"An error occurred while calculating TER score: {str(e)}")
            return 0.0
        
    async def evaluate_async(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        return self.evaluate(reference_sentences, hypothesis_sentences, source_sentences)