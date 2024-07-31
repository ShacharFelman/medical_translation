from services.evaluation.evaluator import EvaluationStrategy
from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import word_tokenize
from utils.logger import logger
from typing import List, Union

class BLEUEvaluator(EvaluationStrategy):
    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        try:
            reference_sentences = [reference_sentences] if isinstance(reference_sentences, str) else reference_sentences
            hypothesis_sentences = [hypothesis_sentences] if isinstance(hypothesis_sentences, str) else hypothesis_sentences

            if not reference_sentences or not hypothesis_sentences:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            tokenized_references = [[word_tokenize(sent.lower())] for sent in reference_sentences]
            tokenized_hypotheses = [word_tokenize(sent.lower()) for sent in hypothesis_sentences]

            bleu_score = corpus_bleu(tokenized_references, tokenized_hypotheses)
            return bleu_score
        except Exception as e:
            logger.error(f"An error occurred while calculating BLEU score: {str(e)}")
            return 0.0