from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import sent_tokenize, word_tokenize

def calculate_bleu(reference_paragraphs, hypothesis_paragraphs):
    # Tokenize paragraphs into sentences, then words
    tokenized_references = [
        [word_tokenize(sent) for sent in sent_tokenize(para.lower())]
        for para in reference_paragraphs
    ]
    tokenized_hypotheses = [
        word_tokenize(sent) 
        for para in hypothesis_paragraphs
        for sent in sent_tokenize(para.lower())
    ]
    
    # Calculate BLEU score
    bleu_score = corpus_bleu([tokenized_references], tokenized_hypotheses)
    
    return bleu_score