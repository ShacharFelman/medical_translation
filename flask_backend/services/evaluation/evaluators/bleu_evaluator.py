from typing import List
from utils.logger import logger
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from utils.constants import BLEUScoreType


class BLEUEvaluator:
    def __init__(self):
        pass

    def evaluate(self, reference: str, 
                 candidate: str, 
                 evaluation_type: str = None) -> float:
        
        try:
            eval_type = evaluation_type.lower()
            ref, cand = self._preprocess_input(reference, candidate, evaluation_type)
               
            if not ref or not cand:
                logger.warning("Empty input: reference or candidate is empty.")
                return 0.0

            if evaluation_type == BLEUScoreType.TOKENIZED_CORPUS.value:
                score = corpus_bleu(ref, cand)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD1.value:
                score = sentence_bleu(ref, cand, smoothing_function=SmoothingFunction().method1)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD7.value:
                score = sentence_bleu(ref, cand, smoothing_function=SmoothingFunction().method7)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value:
                weights = self._calculate_weights(ref, cand)
                score = sentence_bleu(ref, cand, weights=weights, smoothing_function=SmoothingFunction().method1)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD7_WEIGHTS.value:
                weights = self._calculate_weights(ref, cand)
                score = sentence_bleu(ref, cand, weights=weights, smoothing_function=SmoothingFunction().method7)
            else:
                score = corpus_bleu(ref, cand)

            return score

        except Exception as e:
            logger.error(f"An error occurred while calculating BLEU score using {evaluation_type}: {str(e)}")
            return 0.0
    
    async def evaluate_async(self, reference: str, 
                            candidate: str, 
                            source_sentences: str = None) -> float:
        return self.evaluate(reference, candidate, source_sentences)
    

    def _preprocess_input(self, reference: str, candidate: str, evaluation_type: str):
        ref, cand = reference.lower(), candidate.lower()
        if "token" in evaluation_type.lower():
            is_corpus = "corpus" in evaluation_type
            return self._tokenize_input(ref, cand, is_corpus)
        else:
            return self._format_plain_input(ref, cand)


    def _format_plain_input(self, reference, candidate):
        ref = [[reference]]
        cand = [candidate]
        return ref, cand


    def _tokenize_input(self, reference:str , candidate: str, is_corpus: bool):
        ref = [word_tokenize(reference)]
        cand = word_tokenize(candidate)
        if is_corpus:
            ref, cand = [ref], [cand]
        return ref, cand


    def _calculate_weights(self, reference: List[str], candidate: List[str]) -> List[float]:
        ref_length = len(reference[0])
        cand_length = len(candidate)
        max_n = min(4, ref_length, cand_length)
        weights = [1/max_n] * max_n + [0] * (4 - max_n)
        return weights
