import unittest
import json, sys, os
from typing import Dict
from flask_backend.services.evaluation.bleu_score import calculate_bleu
from flask_backend.services.translation_manager import TranslationManager
from flask_backend.data.boundaries import TranslationRequest

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TranslationAccuracyTest(unittest.TestCase):
    def setUp(self):
        translation_service = TranslationManager()
        translation_service.initialize()
        with open('test_data/Sedural.json', 'r', encoding='utf-8') as f:
            self.leaflet_data = json.load(f)

    def test_full_leaflet_translation(self):
        total_bleu_score = 0
        total_sections = 0

        for section in self.leaflet_data['sections']:
            section_bleu_score = self.translate_and_evaluate_section(section)
            if section_bleu_score is not None:
                total_bleu_score += section_bleu_score
                total_sections += 1

        if total_sections > 0:
            average_bleu_score = total_bleu_score / total_sections
            self.assertGreaterEqual(average_bleu_score, 0.60, 
                                    f"Average BLEU score {average_bleu_score} for the entire leaflet is below the threshold of 0.60")
        else:
            self.fail("No valid sections found for translation evaluation")

    def translate_and_evaluate_section(self, section: Dict) -> float:
        section_bleu_scores = []

        for item in section['data']:
            if 'heb' in item and 'eng' in item and item['heb'] != "" and item['eng'] != "":
                translation_request = TranslationRequest(
                    source='he',
                    dest='en',
                    text_input=item['heb']
                )
                translation_response = translation_manager.translate(translation_request, human_verified_translation=item['eng']).translated_text
                if(translation_response != ""):
                    bleu_score = calculate_bleu(item['eng'], translation_response.translated_text)
                    section_bleu_scores.append(bleu_score)

        if section_bleu_scores:
            average_section_bleu = sum(section_bleu_scores) / len(section_bleu_scores)
            print(f"Section '{section['title']}' average BLEU score: {average_section_bleu}")
            return average_section_bleu
        else:
            print(f"No valid items found in section '{section['title']}' for translation evaluation")
            return None

if __name__ == '__main__':
    unittest.main()