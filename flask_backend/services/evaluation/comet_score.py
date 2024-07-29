from evaluate import load
from utils.logger import logger
from typing import List

def calculate_comet(reference_sentences: List[str], hypothesis_sentences: List[str], source_sentences: List[str]) -> float:
    try:
        # Ensure we're working with lists of sentences
        if isinstance(reference_sentences, str):
            reference_sentences = [reference_sentences]
        if isinstance(hypothesis_sentences, str):
            hypothesis_sentences = [hypothesis_sentences]
        if isinstance(source_sentences, str):
            source_sentences = [source_sentences]

        # Check if inputs are empty
        if not reference_sentences or not hypothesis_sentences or not source_sentences:
            logger.warning("Empty input: reference, hypothesis, or source sentences are empty.")
            return 0.0

        # Load COMET metric
        comet = load('comet')

        # Calculate COMET score
        results = comet.compute(
            predictions=hypothesis_sentences,
            references=reference_sentences,
            sources=source_sentences,
            model="Unbabel/wmt22-comet-da"
        )
        
        comet_score = results["mean_score"]
        
        return comet_score

    except Exception as e:
        logger.error(f"An error occurred while calculating COMET score: {str(e)}")
        return 0.0