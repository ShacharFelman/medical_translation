from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import word_tokenize
from utils.logger import logger

def calculate_bleu(reference_sentences, hypothesis_sentences):
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

        # Tokenize sentences into words
        try:
            tokenized_references = [[word_tokenize(sent.lower())] for sent in reference_sentences]
            tokenized_hypotheses = [word_tokenize(sent.lower()) for sent in hypothesis_sentences]
        except AttributeError:
            logger.error("Invalid input: sentences must be strings.")
            return 0.0

        # Calculate BLEU score
        bleu_score = corpus_bleu(tokenized_references, tokenized_hypotheses)
        
        return bleu_score

    except Exception as e:
        logger.error(f"An error occurred while calculating BLEU score: {str(e)}")
        return 0.0