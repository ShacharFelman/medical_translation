from typing import List, Dict, Any
from collections import defaultdict
import numpy as np
from datetime import datetime

class DataProcessor:
    @staticmethod
    def process_translator_performance(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[float]]]:
        performance = defaultdict(lambda: defaultdict(list))
        for record in records:
            for translation in record['translations']:
                translator = translation['translator_name']
                if translation.get('evaluation_scores'):
                    for metric in ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']:
                        if translation['evaluation_scores'].get(metric) is not None:
                            performance[translator][metric].append(translation['evaluation_scores'][metric])
                if translation.get('response_time') is not None:
                    performance[translator]['response_time'].append(translation['response_time'])
                if translation.get('score') is not None:
                    performance[translator]['similarity_score'].append(translation['score'])
        return performance

    @staticmethod
    def calculate_outliers(scores: List[float], threshold: float = 2.0) -> List[float]:
        mean = np.mean(scores)
        std = np.std(scores)
        return [score for score in scores if abs(score - mean) > threshold * std]

    @staticmethod
    def process_time_series_data(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        time_series = defaultdict(list)
        for record in records:
            timestamp = record['timestamp']
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp)
                except ValueError:
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            elif not isinstance(timestamp, datetime):
                continue  # Skip if timestamp is neither string nor datetime
            
            best_translation = record.get('best_translation', {})
            if best_translation.get('evaluation_scores'):
                for metric in ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']:
                    if best_translation['evaluation_scores'].get(metric) is not None:
                        time_series[metric].append({
                            'timestamp': timestamp,
                            'score': best_translation['evaluation_scores'][metric]
                        })
        return time_series

    @staticmethod
    def process_input_complexity(records: List[Dict[str, Any]]) -> Dict[int, Dict[str, List[float]]]:
        complexity = defaultdict(lambda: defaultdict(list))
        for record in records:
            input_length = len(record['input'].split())
            best_translation = record.get('best_translation', {})
            if best_translation.get('evaluation_scores'):
                for metric in ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']:
                    if best_translation['evaluation_scores'].get(metric) is not None:
                        complexity[input_length][metric].append(best_translation['evaluation_scores'][metric])
        return complexity

    @staticmethod
    def calculate_correlations(data: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        metrics = set(metric for item in data for metric in item.keys())
        correlations = {metric: {} for metric in metrics}
        
        for metric1 in metrics:
            for metric2 in metrics:
                if metric1 != metric2:
                    values1 = [item[metric1] for item in data if metric1 in item and metric2 in item]
                    values2 = [item[metric2] for item in data if metric1 in item and metric2 in item]
                    if values1 and values2:
                        correlation = np.corrcoef(values1, values2)[0, 1]
                        correlations[metric1][metric2] = correlation
        
        return correlations