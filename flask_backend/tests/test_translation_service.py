import unittest
from unittest.mock import patch, MagicMock
from services.translation_service import TranslationService
from services.translator import Translator

class TestTranslationService(unittest.TestCase):

    @patch('services.translation_service.MongoDBClient.get_instance')
    @patch('services.translation_service.initialize_translators')
    def setUp(self, mock_initialize_translators, mock_mongo_client):
        # Mock MongoDB client
        self.mock_mongo_instance = MagicMock()
        self.mock_mongo_instance.insert_translation.return_value = MagicMock(inserted_id='mocked_id')
        mock_mongo_client.return_value = self.mock_mongo_instance

        # Mock translators
        self.mock_translator1 = MagicMock(spec=Translator)
        self.mock_translator2 = MagicMock(spec=Translator)
        mock_initialize_translators.return_value = [self.mock_translator1, self.mock_translator2]

        self.translation_service = TranslationService()
        self.translation_service.initialize()

    def test_translate_and_log(self):
        # Mock translation responses
        self.mock_translator1.translate.return_value = {
            "content": "Translated text 1",
            "metadata": {
                "token_usage": {"completion_tokens": 10, "prompt_tokens": 20, "total_tokens": 30},
                "model_name": "gpt-4o",
                "system_fingerprint": "fp_1234567890",
                "finish_reason": "stop",
                "logprobs": None,
                "translation_status": "[TRANSLATION SUCCESSFUL]"
            }
        }
        self.mock_translator2.translate.return_value = {
            "content": "Translated text 2",
            "metadata": {
                "token_usage": {"completion_tokens": 15, "prompt_tokens": 25, "total_tokens": 40},
                "model_name": "claude-3-opus",
                "system_fingerprint": "fp_0987654321",
                "finish_reason": "stop",
                "logprobs": None,
                "translation_status": "[TRANSLATION SUCCESSFUL]"
            }
        }

        # Test input
        input_text = "<heb_text>טקסט בעברית לתרגום</heb_text>"
        human_verified_translation = "Text in Hebrew for translation"

        # Mock time.time() to control elapsed time
        with patch('time.time', side_effect=[0, 1, 2, 3, 4]):
            result = self.translation_service.translate(input_text, human_verified_translation)

        # Assert the result
        self.assertEqual(result, "Translated text 1")

        # Assert that MongoDB insert was called
        self.mock_mongo_instance.insert_translation.assert_called_once()
        inserted_data = self.mock_mongo_instance.insert_translation.call_args[0][0]
        
        self.assertEqual(inserted_data['input_text'], input_text)
        self.assertEqual(len(inserted_data['translations']), 2)
        
        for translation in inserted_data['translations']:
            self.assertIn('llm_name', translation)
            self.assertIn('output', translation)
            self.assertIn('input_tokens', translation)
            self.assertIn('output_tokens', translation)
            self.assertIn('response_time', translation)
            self.assertIn('bleu_score', translation)

        # Assert that calculate_bleu was called for each translation
        with patch('services.translation_service.calculate_bleu') as mock_calculate_bleu:
            mock_calculate_bleu.return_value = 0.8
            self.translation_service.translate(input_text, human_verified_translation)
            self.assertEqual(mock_calculate_bleu.call_count, 2)

    def test_mongodb_error_handling(self):
        # Set up MongoDB to raise an exception
        self.mock_mongo_instance.insert_translation.side_effect = Exception("MongoDB connection error")

        input_text = "<heb_text>טקסט לבדיקת שגיאה</heb_text>"

        # Ensure that the translation still works even if MongoDB fails
        with self.assertLogs(level='ERROR') as log:
            result = self.translation_service.translate(input_text)

        self.assertIn("Failed to save translation to MongoDB", log.output[0])
        self.assertEqual(result, "Translated text 1")

if __name__ == '__main__':
    unittest.main()