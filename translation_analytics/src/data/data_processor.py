from typing import List, Dict, Any
from collections import defaultdict

class DataProcessor:
    @staticmethod
    def process_translator_performance(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        performance = defaultdict(lambda: defaultdict(list))
        for record in records:
            for translation in record['translations']:
                translator = translation['translator_name']
                if translation.get('evaluation_scores'):
                    if translation['evaluation_scores'].get('bleu_score') is not None:
                        performance[translator]['bleu'].append(translation['evaluation_scores']['bleu_score'])
                    if translation['evaluation_scores'].get('comet_score') is not None:
                        performance[translator]['comet'].append(translation['evaluation_scores']['comet_score'])
                if translation.get('response_time') is not None:
                    performance[translator]['response_time'].append(translation['response_time'])
                if translation.get('score') is not None:
                    performance[translator]['score'].append(translation['score'])

        return {
            translator: {
                metric: sum(scores) / len(scores) 
                for metric, scores in metrics.items() 
                if scores
            }
            for translator, metrics in performance.items()
        }
    

    @staticmethod
    def process_leaflet_performance(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        performance = defaultdict(lambda: defaultdict(list))
        for record in records:
            if record.get('evaluation_leaflet_data'):
                leaflet_id = record['evaluation_leaflet_data']['leaflet_id']
                best_translation = record.get('best_translation', {})
                if best_translation.get('evaluation_scores'):
                    performance[leaflet_id]['bleu'].append(best_translation['evaluation_scores'].get('bleu_score'))
                    performance[leaflet_id]['comet'].append(best_translation['evaluation_scores'].get('comet_score'))
                performance[leaflet_id]['response_time'].append(best_translation.get('response_time'))

        return {leaflet: {metric: sum(scores)/len(scores) for metric, scores in metrics.items() if scores}
                for leaflet, metrics in performance.items()}

    @staticmethod
    def process_bleu_score_data(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        translator_performance = defaultdict(list)
        input_complexity = defaultdict(list)
        time_performance = []
        metric_correlation = []
        efficiency_quality = []

        for record in records:
            for translation in record['translations']:
                if translation.get('evaluation_scores') and translation['evaluation_scores'].get('bleu_score'):
                    translator_performance[translation['translator_name']].append(translation['evaluation_scores']['bleu_score'])

            input_length = len(record['input'].split())
            if record['best_translation'] and record['best_translation'].get('evaluation_scores'):
                bleu_score = record['best_translation']['evaluation_scores'].get('bleu_score')
                if bleu_score:
                    input_complexity[input_length].append(bleu_score)
                    time_performance.append({
                        'timestamp': record['timestamp'],
                        'bleu_score': bleu_score
                    })
                    metric_correlation.append({
                        'bleu_score': bleu_score,
                        'comet_score': record['best_translation']['evaluation_scores'].get('comet_score'),
                        'similarity_score': record['best_translation'].get('score')
                    })
                    efficiency_quality.append({
                        'response_time': record['best_translation'].get('response_time'),
                        'bleu_score': bleu_score
                    })

        return {
            'translator_performance': {t: sum(scores)/len(scores) for t, scores in translator_performance.items()},
            'input_complexity': {length: sum(scores)/len(scores) for length, scores in input_complexity.items()},
            'time_performance': sorted(time_performance, key=lambda x: x['timestamp']),
            'metric_correlation': metric_correlation,
            'efficiency_quality': efficiency_quality
        }