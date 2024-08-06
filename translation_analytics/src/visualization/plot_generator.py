import matplotlib.pyplot as plt
from typing import Dict, List, Any

class PlotGenerator:
    @staticmethod
    def plot_translator_performance(data: Dict[str, Dict[str, float]], metric: str):
        translators = list(data.keys())
        values = [metrics.get(metric, 0) for metrics in data.values()]

        plt.figure(figsize=(10, 6))
        plt.bar(translators, values)
        plt.title(f'Translator Performance - {metric.capitalize()}')
        plt.xlabel('Translator')
        plt.ylabel(metric.capitalize())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'/app/output/translator_performance_{metric}.png')
        plt.close()


    @staticmethod
    def plot_leaflet_performance(data: Dict[str, Dict[str, float]], metric: str):
        leaflets = list(data.keys())
        values = [metrics.get(metric, 0) for metrics in data.values()]

        plt.figure(figsize=(10, 6))
        plt.bar(leaflets, values)
        plt.title(f'Leaflet Performance - {metric.capitalize()}')
        plt.xlabel('Leaflet ID')
        plt.ylabel(metric.capitalize())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'/app/output/leaflet_performance_{metric}.png')
        plt.close()

    @staticmethod
    def plot_bleu_insights(data: Dict[str, Any]):
        # Input Complexity vs BLEU Score
        plt.figure(figsize=(10, 6))
        plt.scatter(data['input_complexity'].keys(), data['input_complexity'].values())
        plt.title('Input Complexity vs BLEU Score')
        plt.xlabel('Input Length (words)')
        plt.ylabel('Average BLEU Score')
        plt.tight_layout()
        plt.savefig('/app/output/input_complexity_bleu.png')
        plt.close()

        # BLEU vs COMET Scores
        plt.figure(figsize=(10, 6))
        plt.scatter([item['bleu_score'] for item in data['metric_correlation']], 
                    [item['comet_score'] for item in data['metric_correlation']])
        plt.title('BLEU vs COMET Scores')
        plt.xlabel('BLEU Score')
        plt.ylabel('COMET Score')
        plt.tight_layout()
        plt.savefig('/app/output/bleu_vs_comet.png')
        plt.close()
