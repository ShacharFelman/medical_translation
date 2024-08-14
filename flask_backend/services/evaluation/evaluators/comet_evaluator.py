import requests
import aiohttp
from utils.logger import logger
from typing import List, Union
import json

class COMETEvaluator():
    def __init__(self):
        self.api_url = "https://evaluate-metric-comet.hf.space/run/predict"

    def evaluate(self, reference:str, 
                 candidate: str, 
                 source: str = None) -> float:
        try:
            reference, candidate, source = self._preprocess_input(reference, candidate, source)

            if not reference or not candidate or not source:
                logger.warning("Empty input: reference, candidate, or source sentences are empty.")
                return 0.0

            data = {
                "data": [
                    {
                        "headers": ["sources", "predictions", "references"],
                        "data": [[src, pred, ref] for src, pred, ref in zip(source, candidate, reference)]
                    }
                ]
            }
            
            response = requests.post(self.api_url, json=data)
            response_data = response.json()

            if response.status_code == 200 and "data" in response_data:
                comet_data_str = response_data["data"][0].replace("'", '"')
                comet_data = json.loads(comet_data_str)
                comet_score = comet_data["mean_score"]
                logger.info(f"COMET response time: {response_data['duration']}")
                return comet_score
            else:
                logger.error(f"Failed to get a valid response from COMET API: {response_data}")
                return 0.0

        except Exception as e:
            logger.error(f"An error occurred while calculating COMET score: {str(e)}")
            return 0.0


    async def evaluate_async(self, reference: Union[str, List[str]], 
                             candidate: Union[str, List[str]], 
                             source: Union[str, List[str]] = None) -> float:
        try:
            reference, candidate, source = self._preprocess_input(reference, candidate, source)

            if not reference or not candidate or not source:
                logger.warning("Empty input: reference, candidate, or source sentences are empty.")
                return 0.0

            data = {
                "data": [
                    {
                        "headers": ["sources", "predictions", "references"],
                        "data": [[src, pred, ref] for src, pred, ref in zip(reference, candidate, source)]
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        if "data" in response_data:
                            comet_data_str = response_data["data"][0].replace("'", '"')
                            comet_data = json.loads(comet_data_str)
                            comet_score = comet_data["mean_score"]
                            logger.info(f"COMET response time: {response_data['duration']}")
                            return comet_score
                        else:
                            logger.error(f"Unexpected response structure from COMET API: {response_data}")
                    else:
                        logger.error(f"Failed to get a valid response from COMET API. Status: {response.status}\nResponse: {response}")
                    
            logger.error("COMET evaluation failed")
            return 0.0

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse COMET API response: {str(e)}")
            return 0.0
        except KeyError as e:
            logger.error(f"Expected key not found in COMET API response: {str(e)}")
            return 0.0
        except Exception as e:
            logger.error(f"An unexpected error occurred while calculating COMET score asynchronously: {str(e)}")
            return 0.0
        

    def _preprocess_input(self, reference: str, candidate: str, source: str):
        ref, cand = reference.lower(), candidate.lower()
        ref     = [reference]
        cand    = [candidate]
        source  = [source]
        return ref, cand