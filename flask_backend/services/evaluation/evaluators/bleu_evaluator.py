import unicodedata
import string
from typing import List
from utils.logger import logger
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from utils.constants import BLEUScoreType

class BLEUEvaluator:
    def __init__(self):
        self.translator = str.maketrans('', '', string.punctuation)


    def evaluate(self,
                 reference: str, 
                 candidate: str, 
                 evaluation_type: str = None) -> float:
        
        try:
            eval_type = evaluation_type.lower()
            ref, cand = self._preprocess_input(reference, candidate, eval_type)
               
            if not ref or not cand:
                logger.warning("Empty input: reference or candidate is empty.")
                return 0.0

            if evaluation_type == BLEUScoreType.TOKENIZED_CORPUS.value:
                score = corpus_bleu(ref, cand)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD1.value:
                score = sentence_bleu(ref, cand, smoothing_function=SmoothingFunction().method1)
            elif evaluation_type == BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value:
                weights = self._calculate_weights(ref, cand)
                score = sentence_bleu(ref, cand, weights=weights, smoothing_function=SmoothingFunction().method1)
            else:
                score = corpus_bleu(ref, cand)

            return score

        except Exception as e:
            logger.error(f"An error occurred while calculating BLEU score using {eval_type}: {str(e)}")
            return 0.0
    
    async def evaluate_async(self, reference: str, 
                            candidate: str, 
                            source_sentences: str = None) -> float:
        return self.evaluate(reference, candidate, source_sentences)
    

    def _preprocess_input(self, reference: str, candidate: str, evaluation_type: str):
        try:
            ref, cand = self._preprocess_text(reference), self._preprocess_text(candidate)
            tokenize = "token" in evaluation_type.lower()
            corpus = "corpus" in evaluation_type
            ref     = self._preprocess_text(reference, tokenize=tokenize)
            cand    = self._preprocess_text(candidate, tokenize=tokenize)
            if tokenize:
                ref, cand = self._format_tokenized_input(ref, cand, corpus)
            else:
                ref, cand = self._format_plain_input(ref, cand)
            
            return ref, cand

        except Exception as e:
            logger.error(f"An error occurred while preprocessing input: {str(e)}")
            return None, None

    def _format_plain_input(self, reference, candidate):
        ref = [[reference]]
        cand = [candidate]
        return ref, cand


    def _format_tokenized_input(self, reference: List[str], candidate: List[str], is_corpus: bool):
        ref = [reference]
        cand = candidate
        if is_corpus:
            ref, cand = [ref], [cand]
        return ref, cand

    def _calculate_weights(self, reference: List[str], candidate: List[str]) -> List[float]:
        ref_length = len(reference[0])
        cand_length = len(candidate)
        max_n = min(4, ref_length, cand_length)
        weights = [1/max_n] * max_n + [0] * (4 - max_n)
        return weights
    
    def _preprocess_text(self, text, tokenize=True, lowercase=True, remove_punct=True, normalize=True):
        procesessed_text = text
        if tokenize:
            procesessed_text = self.tokenize(text)
        if lowercase:
            procesessed_text = self.lowercase(procesessed_text, tokenize)
        if remove_punct:
            procesessed_text = self.remove_punctuation(procesessed_text, tokenize)
        if normalize:
            procesessed_text = self.normalize(procesessed_text, tokenize)

        procesessed_text = self.remove_extra_whitespace(procesessed_text, tokenize)
        return procesessed_text

    def tokenize(self, text):
        return word_tokenize(text)

    def lowercase(self, text, tokenized=True):
        return [token.lower() for token in text] if tokenized else text.lower()

    def remove_punctuation(self, text, tokenized=True):
        return [token for token in text if token.isalnum()] if tokenized else text.translate(self.translator)

    def normalize(self, text, tokenized=True):
        return [self.normalize_text(token) for token in text] if tokenized else self.normalize_text(text)

    def normalize_text(self, text):
        return ''.join(c for c in unicodedata.normalize('NFKD', text) 
            if not unicodedata.combining(c))

    def remove_extra_whitespace(self, text, tokenized):
        return [token.strip() for token in text if token.strip()] if tokenized else text.strip()
