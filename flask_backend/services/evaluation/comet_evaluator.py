from services.evaluation.evaluator import EvaluationStrategy
import requests
from utils.logger import logger
from typing import List, Union
import json


class COMETEvaluator(EvaluationStrategy):
    def __init__(self):
        self.api_url = "https://evaluate-metric-comet.hf.space/run/predict"

    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        try:
            reference_sentences = [reference_sentences] if isinstance(reference_sentences, str) else reference_sentences
            hypothesis_sentences = [hypothesis_sentences] if isinstance(hypothesis_sentences, str) else hypothesis_sentences
            source_sentences = [source_sentences] if isinstance(source_sentences, str) else source_sentences

            if not reference_sentences or not hypothesis_sentences or not source_sentences:
                logger.warning("Empty input: reference, hypothesis, or source sentences are empty.")
                return 0.0

            data = {
                "data": [
                    {
                        "headers": ["sources", "predictions", "references"],
                        "data": [[src, hyp, ref] for src, hyp, ref in zip(source_sentences, hypothesis_sentences, reference_sentences)]
                    }
                ]
            }
            
            response = requests.post(self.api_url, json=data)
            response_data = response.json()

            if response.status_code == 200 and "data" in response_data:
                comet_data_str = response_data["data"][0].replace("'", '"')
                comet_data = json.loads(comet_data_str)
                comet_score = comet_data["mean_score"]
                return comet_score
            else:
                logger.error(f"Failed to get a valid response from COMET API: {response_data}")
                return 0.0

        except Exception as e:
            logger.error(f"An error occurred while calculating COMET score: {str(e)}")
            return 0.0
