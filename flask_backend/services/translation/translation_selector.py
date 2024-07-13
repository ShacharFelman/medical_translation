from langchain_voyageai import VoyageAIEmbeddings
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.logger import logger
import os
from data.entities import TranslationEntity

class TranslationSelector:
    def __init__(self):
        api_key_voyageai = os.getenv('API_KEY_VOYAGEAI')
        self.embedding_model = VoyageAIEmbeddings(voyage_api_key=api_key_voyageai, model='voyage-large-2-instruct')

    def select_best_translation(self, translations: List[TranslationEntity]) -> Tuple[TranslationEntity, np.ndarray]:
        if not translations:
            logger.warning("No translations provided for selection.")
            return None, np.array([])

        if len(translations) == 1:
            logger.info("Only one translation provided. Returning it as the best.")
            return translations[0], np.array([1.0])

        try:
            # Extract translation texts
            translation_texts = [t.translated_text for t in translations]
            logger.debug(f"Translation texts: {translation_texts}")

            # Generate embeddings for all translations
            embeddings = self.embedding_model.embed_documents(translation_texts)
            logger.debug(f"Embeddings shape: {np.array(embeddings).shape}")

            # Calculate cosine similarities
            similarities = cosine_similarity(embeddings)
            logger.debug(f"Similarities shape: {similarities.shape}")

            # Calculate average similarity for each translation
            average_similarities = (similarities.sum(axis=1) - 1) / (len(translations) - 1)  # Subtract 1 to remove self-similarity
            logger.debug(f"Average similarities: {average_similarities}")

            # Select the translation with the highest average similarity
            best_index = np.argmax(average_similarities)
            best_translation = translations[best_index]

            logger.info(f"Selected best translation from translator: {best_translation.translator_name}")
            return best_translation, average_similarities
        except Exception as e:
            logger.error(f"Error in select_best_translation: {str(e)}")
            logger.error(f"Translations: {translations}")
            raise

translation_selector = TranslationSelector()