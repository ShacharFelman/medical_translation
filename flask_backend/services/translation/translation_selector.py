from langchain_voyageai import VoyageAIEmbeddings
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.logger import logger
import os

api_key_voyageai = os.getenv('API_KEY_VOYAGEAI')


class TranslationSelector:
    def __init__(self):
        self.embedding_model = VoyageAIEmbeddings(voyage_api_key= api_key_voyageai, model='voyage-large-2-instruct')

    def select_best_translation(self, translations: List[Dict[str, Any]]) -> tuple[Dict[str, Any], np.ndarray]:
        if not translations:
            logger.warning("No translations provided for selection.")
            return None, np.array([])

        if len(translations) == 1:
            logger.info("Only one translation provided. Returning it as the best.")
            return translations[0], np.array([1.0])

        # Extract translation texts
        translation_texts = [t['output'] for t in translations]

        # Generate embeddings for all translations
        embeddings = self.embedding_model.embed_documents(translation_texts)

        # Calculate cosine similarities
        similarities = cosine_similarity(embeddings)

        # Calculate average similarity for each translation
        average_similarities = (similarities.sum(axis=1) - 1) / (len(translations) - 1) # Subtract 1 to remove self-similarity

        # Select the translation with the highest average similarity
        best_index = np.argmax(average_similarities)
        best_translation = translations[best_index]

        logger.info(f"Selected best translation from translator: {best_translation['model_name']}")
        return best_translation, average_similarities
    
translation_selector = TranslationSelector()