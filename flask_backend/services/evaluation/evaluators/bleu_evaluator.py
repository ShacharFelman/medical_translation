from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
from utils.logger import logger
from typing import List, Union



class BLEUEvaluator:
    def __init__(self):
        pass

    def evaluate(self, reference_sentences: str, 
                 hypothesis_sentences: str, 
                 source_sentences: str = None,
                 evaluation_type: str = None) -> float:
        
        tokenization = False
        is_corpus = False
        formated_reference_sentence, formated_hypothesis_sentence = self._lowercase_input(reference_sentences, hypothesis_sentences)
        if "token" in evaluation_type:
            tokenization = True
        if "corpus" in evaluation_type:
            is_corpus = True
        
        try:

            if tokenization:
               formated_reference_sentence, formated_hypothesis_sentence = self._tokkenize_evaluator_input(formated_reference_sentence, formated_hypothesis_sentence, is_corpus)
            else:
                formated_reference_sentence, formated_hypothesis_sentence = self._format_evaluator_plain_input(formated_reference_sentence, formated_hypothesis_sentence)

            if not formated_reference_sentence or not formated_hypothesis_sentence:
                logger.warning("Empty input: reference or hypothesis sentences are empty.")
                return 0.0

            if evaluation_type == "plain_corpus":
                score = corpus_bleu(formated_reference_sentence, formated_hypothesis_sentence)
            elif evaluation_type == "token_meth1":
                score = sentence_bleu(formated_reference_sentence, formated_hypothesis_sentence, smoothing_function=SmoothingFunction().method1)
            elif evaluation_type == "token_meth7":
                score = sentence_bleu(formated_reference_sentence, formated_hypothesis_sentence, smoothing_function=SmoothingFunction().method7)
            elif evaluation_type == "token_meth1_w":
                weights = self._calculate_weights(formated_reference_sentence, formated_hypothesis_sentence)
                score = sentence_bleu(formated_reference_sentence, formated_hypothesis_sentence, weights=weights, smoothing_function=SmoothingFunction().method1)
            elif evaluation_type == "token_meth7_w":
                weights = self._calculate_weights(formated_reference_sentence, formated_hypothesis_sentence)
                score = sentence_bleu(formated_reference_sentence, formated_hypothesis_sentence, weights=weights, smoothing_function=SmoothingFunction().method7)
            else:
                score = corpus_bleu(formated_reference_sentence, formated_hypothesis_sentence)

            return score

        except Exception as e:
            logger.error(f"An error occurred while calculating BLEU score: {str(e)}")
            return 0.0
    
    async def evaluate_async(self, reference_sentences: str, 
                            hypothesis_sentences: str, 
                            source_sentences: str = None) -> float:
        return self.evaluate(reference_sentences, hypothesis_sentences, source_sentences)
    

    def _lowercase_input(self, reference_sentences: str, hypothesis_sentences: str):
        return reference_sentences.lower(), hypothesis_sentences.lower()


    def _format_evaluator_plain_input(self, reference_sentences: str, 
                                hypothesis_sentences: str):
        formated_reference_sentences = [[reference_sentences]] if isinstance(reference_sentences, str) else reference_sentences
        formated_hypothesis_sentences = [hypothesis_sentences] if isinstance(hypothesis_sentences, str) else hypothesis_sentences
        return formated_reference_sentences, formated_hypothesis_sentences


    def _tokkenize_evaluator_input(self, reference_sentences: str, hypothesis_sentences: str, is_corpus: bool):
        reference = [word_tokenize(reference_sentences)]
        hypothesis = word_tokenize(hypothesis_sentences)

        return ([reference], [hypothesis]) if is_corpus else (reference, hypothesis)


    def _calculate_weights(self, reference_sentence, hypothesis_sentence):
        ref_length = len(reference_sentence[0])
        cand_length = len(hypothesis_sentence)
        max_n = min(4, ref_length, cand_length)
        weights = [1/max_n] * max_n + [0] * (4 - max_n)
        return weights

    # def flatten(item):
    #     if isinstance(item, str):
    #         return item
    #     elif isinstance(item, list):
    #         return ' '.join(flatten(subitem) for subitem in item if subitem is not None)
    #     else:
    #         raise ValueError(f"Unexpected input type: {type(item)}")
    
    # reference = [[flatten(reference_sentences)]]
    # hypothesis = [flatten(hypothesis_sentences)]
    
    # return reference, hypothesis
       