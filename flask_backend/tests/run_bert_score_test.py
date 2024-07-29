import os
import sys
from services.evaluation.bert_score import calculate_bert_score
from services.evaluation.comet_score import calculate_comet_score

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.translation_manager import TranslationManager

def run_bert_score_test():

    machine_translation = ["The doctor is beutiful"]
    human_translation = ["The physician is pretty"]

    result = calculate_bert_score(human_translation, machine_translation)

    print(f"Translation result: {result}")


def run_comet_score_test():

    machine_translation = ["The doctor is beutiful"]
    human_translation = ["The physician is pretty"]
    source_text = ["הדוקטור יפה"]

    result = calculate_comet_score(human_translation, machine_translation, source_text)

    print(f"Translation result: {result}")

if __name__ == "__main__":
    # run_bert_score_test()
    calculate_comet_score()