from langchain_voyageai import VoyageAIEmbeddings
from typing import List, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.logger import logger
import os
from data.entities import TranslationEntity

class TranslationSelector:
    def __init__(self):
        api_key_voyageai = os.getenv('API_KEY_VOYAGEAI')
        self.embedding_model = VoyageAIEmbeddings(voyage_api_key=api_key_voyageai, model='voyage-large-2-instruct')

    def select_best_translation(self, translations: List[TranslationEntity]) -> Tuple[Optional[TranslationEntity], np.ndarray]:
        if not translations:
            logger.warning("No translations provided for selection.")
            return None, np.array([])

        if len(translations) == 1:
            logger.info("Only one translation provided. Returning it as the best.")
            return translations[0], np.array([1.0])

        try:
            translation_texts = [t.translated_text for t in translations]
            
            if not all(translation_texts):
                logger.error("One or more translations have empty text.")
                return None, np.array([])

            embeddings = self._generate_embeddings(translation_texts)
            
            if embeddings is None or len(embeddings) != len(translations):
                logger.error("Failed to generate embeddings for all translations.")
                return None, np.array([])

            similarities = self._calculate_similarities(embeddings)
            
            if similarities is None:
                logger.error("Failed to calculate similarities between translations.")
                return None, np.array([])

            average_similarities = self._calculate_average_similarities(similarities)
            
            if average_similarities is None:
                logger.error("Failed to calculate average similarities.")
                return None, np.array([])

            best_index = np.argmax(average_similarities)
            best_translation = translations[best_index]

            logger.info(f"Selected best translation from translator: {best_translation.translator_name}")
            return best_translation, average_similarities

        except Exception as e:
            logger.error(f"Error in select_best_translation: {str(e)}")
            return None, np.array([])

    def _generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        try:
            return self.embedding_model.embed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return None

    def _calculate_similarities(self, embeddings: List[List[float]]) -> Optional[np.ndarray]:
        try:
            return cosine_similarity(embeddings)
        except Exception as e:
            logger.error(f"Error calculating cosine similarities: {str(e)}")
            return None

    def _calculate_average_similarities(self, similarities: np.ndarray) -> Optional[np.ndarray]:
        try:
            return (similarities.sum(axis=1) - 1) / (len(similarities) - 1)
        except Exception as e:
            logger.error(f"Error calculating average similarities: {str(e)}")
            return None

translation_selector = TranslationSelector()