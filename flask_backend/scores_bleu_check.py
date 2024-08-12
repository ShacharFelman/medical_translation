
from services.evaluation.bleu_evaluator import BLEUEvaluator
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from utils.logger import logger

bleu_evaluator = BLEUEvaluator()

def calculate_blue_from_evaluator():
    human_translation = "• Skin tags"
    translated_text = "• Skin tags"
    
    bleu_score = bleu_evaluator.evaluate(
        reference_sentences=[human_translation],
        hypothesis_sentences=[translated_text]
    )

    logger.info(f"BLEU score: {bleu_score}")


def calculate_bleu():
    chencherry = SmoothingFunction()

    # Example usage
    reference = [["Side effects of unknown frequency"]]
    candidate = ["Side effects of unknown frequency"]

    ref_length = len(reference[0])
    cand_length = len(candidate)
    max_n = min(4, ref_length, cand_length)
    weights = [1/max_n] * max_n + [0] * (4 - max_n)
    score_method1 = sentence_bleu(reference, candidate, weights=weights, smoothing_function=SmoothingFunction().method1)
    score_method7 = sentence_bleu(reference, candidate, weights=weights, smoothing_function=SmoothingFunction().method7)

    logger.info(f"BLEU score method1: {score_method1}")
    logger.info(f"BLEU score method7: {score_method7}")


if __name__ == "__main__":
    calculate_bleu()