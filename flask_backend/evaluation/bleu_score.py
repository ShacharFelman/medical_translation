import nltk
from nltk.translate.bleu_score import sentence_bleu

def calculate_bleu(reference_translations, hypothesis_translation):
    # Tokenize the reference translations and hypothesis translation
    reference_translations = [nltk.word_tokenize(ref) for ref in reference_translations]
    hypothesis_translation = nltk.word_tokenize(hypothesis_translation)

    # Calculate the BLEU score
    bleu_score = sentence_bleu(reference_translations, hypothesis_translation)

    return bleu_score