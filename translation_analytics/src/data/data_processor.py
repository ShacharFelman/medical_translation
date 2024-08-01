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
                    performance[translator]['bleu'].append(translation['evaluation_scores'].get('bleu_score'))
                    performance[translator]['comet'].append(translation['evaluation_scores'].get('comet_score'))
                performance[translator]['response_time'].append(translation['response_time'])
                performance[translator]['score'].append(translation.get('score'))

        return {translator: {metric: sum(scores)/len(scores) for metric, scores in metrics.items() if scores}
                for translator, metrics in performance.items()}

    @staticmethod
    def process_system_performance_over_time(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        performance = sorted(
            [{'timestamp': r['timestamp'],
              'bleu': r['best_translation']['evaluation_scores'].get('bleu_score'),
              'comet': r['best_translation']['evaluation_scores'].get('comet_score'),
              'response_time': r['best_translation']['response_time']}
             for r in records if r.get('best_translation')],
            key=lambda x: x['timestamp']
        )
        return performance

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