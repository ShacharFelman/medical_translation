from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from utils.constants import BLEUScoreType
bleu_evaluator = BLEUEvaluator()
#############################################

machine_str =   """
Uncommon side effects (may affect up to 1 in 100 people):

Breathing difficulties, yawning, swelling of the face or hands and feet, inflammation or infection of the tongue, skin rash, itching, increased sensitivity to touch or pain, loss of coordination, slowing or difficulty in movement, tremor, speech disorder, feeling detached from yourself, depression, strange thoughts, irritability, confusion, mood swings (euphoria), states of sensory clouding, general discomfort, feeling unwell, insomnia, loss of appetite and weight loss (anorexia), taste disturbance, thirst, joint degeneration (arthrosis), bone pain, joint pain, increased need to urinate, urinary disturbances, excessive urination, diarrhea, abnormal vision, eye pain, light intolerance, dry or watery eyes, ear pain, ringing in the ears (tinnitus), blood flow disturbance (peripheral vascular disease).
                """

human_str =     """
Uncommon side effects (may affect up to 1 in 100 people):
Difficulty breathing, yawning, swelling of the face or hands and feet, inflammation or infection of the tongue, skin rash, itching, increased sense of touch or pain, loss of co-ordination, slow or reduced movement, tremor, slurred speech, not feeling one self (depersonalisation), depression, thinking strangely, feeling agitated, feeling confused, mood swings (euphoria), periods of unresponsiveness (stupor), general feeling of discomfort, malaise, sleeplessness, loss of appetite and weight loss (anorexia), taste disturbance, thirst, degeneration of the joints (arthrosis), bone pain, joint pain, increased need to urinate, problems with urinating, passing excessive quantity of urine, diarrhoea, abnormal vision, eye pain, intolerance to light, dry or watery eyes, ear pain, ringing in the ears (tinnitus), poor circulation (peripheral vascular disorder).
                """

#############################################

try:

    score = bleu_evaluator.evaluate(human_str, machine_str, BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value)
    print(f"BLEU score: {score}")

except Exception as e:
    print(f"Error calculating BLEU score: {str(e)}")
