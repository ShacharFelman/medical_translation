
from services.evaluation.bleu_evaluator import BLEUEvaluator
from utils.logger import logger

bleu_evaluator = BLEUEvaluator()

def calculate_blue():
    human_translation = "Do not use this medicine if:"
    translated_text = "Do not use the medication if:"
    
    bleu_score = bleu_evaluator.evaluate(
        reference_sentences=[human_translation],
        hypothesis_sentences=[translated_text]
    )

    logger.info(f"BLEU score: {bleu_score}")


if __name__ == "__main__":
    calculate_blue()