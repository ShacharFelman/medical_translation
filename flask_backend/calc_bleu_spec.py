from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from utils.constants import BLEUScoreType

bleu_evaluator = BLEUEvaluator()
#############################################

machine_str =   """
Swelling of the face, lips, or tongue

                """

human_str =     """
•	Swelling of the face, lips, mouth or tongue

                """

#############################################

try:

    score = bleu_evaluator.evaluate(human_str, machine_str, BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value)
    print(f"BLEU score: {score}")

except Exception as e:
    print(f"Error calculating BLEU score: {str(e)}")
