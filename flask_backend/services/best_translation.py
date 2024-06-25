import os
from utils.logger import logger
from utils.singleton_meta import SingletonMeta
from langchain_voyageai import VoyageAIEmbeddings
from services.prompt_templates import translation_success_string

api_key_voyageai = os.getenv('API_KEY_VOYAGEAI')


class TranslationSelector(metaclass=SingletonMeta):
    def __init__(self):
        self.embedding_model = VoyageAIEmbeddings(voyage_api_key=api_key_voyageai, model="voyage-large-2-instruct")
        
    def generate_embeddings(self, texts):
            return self.embedding_model.embed_documents(texts)

    def select_best_translation(self, translations):
        # Filter out only successful translations

        logger.debug(f'1) translations: {translations}')

        successful_translations = [
            translation for translation in translations if translation['status'] == translation_success_string
        ]

        logger.debug(f'2) successful translations: {successful_translations}')

        if not successful_translations:
            return None

        # Extract texts from successful translations
        texts = [translation['translated_text'] for translation in successful_translations]

        # Generate embeddings for all successful translations
        embeddings = self.generate_embeddings(texts)

        # Pair each translation with its corresponding embedding
        translation_embeddings = list(zip(successful_translations, embeddings))

        logger.debug(f'Translation embeddings: {translation_embeddings}')

transltion_selector = TranslationSelector()