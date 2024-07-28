from evaluate import load
from typing import List
from utils.logger import logger

bertscore = load("bertscore")

def calculate_bert_score(reference_sentences: List[str], hypothesis_sentences: List[str]):
    try:
        # Ensure we're working with lists of sentences
        if isinstance(reference_sentences, str):
            reference_sentences = [reference_sentences]
        if isinstance(hypothesis_sentences, str):
            hypothesis_sentences = [hypothesis_sentences]

        # Check if inputs are empty
        if not reference_sentences or not hypothesis_sentences:
            logger.warning("Empty input: reference or hypothesis sentences are empty.")
            return 0.0

        # Calculate BERT Score
        results = bertscore.compute(predictions=hypothesis_sentences, references=reference_sentences, model_type="distilbert-base-uncased")
        
        # We'll use the average F1 score as our primary metric
        bert_score = sum(results['f1']) / len(results['f1'])

        return bert_score

    except Exception as e:
        logger.error(f"An error occurred while calculating BERT Score: {str(e)}")
        return 0.0
    
