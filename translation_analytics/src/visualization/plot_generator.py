# File: visualization/plot_generator.py

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
import numpy as np
from datetime import datetime
from collections import defaultdict

class PlotGenerator:
    @staticmethod
    def plot_translator_performance(data: Dict[str, Dict[str, List[float]]], metric: str):
        plt.figure(figsize=(12, 6))
        translators = list(data.keys())
        values = [np.mean(metrics.get(metric, [])) for metrics in data.values()]

        plt.bar(translators, values)
        plt.title(f'Translator Performance - {metric.capitalize()}')
        plt.xlabel('Translator')
        plt.ylabel(f'Average {metric.capitalize()}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'/app/output/translator_performance_{metric}.png')
        plt.close()

    @staticmethod
    def plot_input_complexity(data: Dict[int, Dict[str, List[float]]]):
        plt.figure(figsize=(12, 6))
        lengths = list(data.keys())
        metrics = ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']
        
        for metric in metrics:
            values = [np.mean(data[length].get(metric, [])) for length in lengths]
            plt.plot(lengths, values, label=metric.upper())

        plt.title('Input Complexity vs. Translation Quality')
        plt.xlabel('Input Length (words)')
        plt.ylabel('Average Score')
        plt.legend()
        plt.tight_layout()
        plt.savefig('/app/output/input_complexity.png')
        plt.close()

    @staticmethod
    def plot_time_series(data: Dict[str, List[Dict[str, Any]]]):
        plt.figure(figsize=(12, 6))
        metrics = list(data.keys())
        
        for metric in metrics:
            timestamps = []
            scores = []
            for item in data[metric]:
                timestamp = item['timestamp']
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp)
                    except ValueError:
                        # If fromisoformat fails, try a different parsing method
                        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                elif not isinstance(timestamp, datetime):
                    # If it's neither string nor datetime, skip this item
                    continue
                timestamps.append(timestamp)
                scores.append(item['score'])
            
            if timestamps and scores:
                plt.plot(timestamps, scores, label=metric.upper())

        plt.title('Translation Quality Over Time')
        plt.xlabel('Date')
        plt.ylabel('Score')
        plt.legend()
        plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
        plt.tight_layout()
        plt.savefig('/app/output/time_series.png')
        plt.close()
        
    @staticmethod
    def plot_correlations(data: Dict[str, Dict[str, float]]):
        metrics = list(data.keys())
        corr_matrix = np.zeros((len(metrics), len(metrics)))
        
        for i, metric1 in enumerate(metrics):
            for j, metric2 in enumerate(metrics):
                if i == j:
                    corr_matrix[i, j] = 1.0
                elif j > i:
                    corr_matrix[i, j] = data[metric1].get(metric2, 0)
                else:
                    corr_matrix[i, j] = data[metric2].get(metric1, 0)

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', xticklabels=metrics, yticklabels=metrics)
        plt.title('Correlation Between Metrics')
        plt.tight_layout()
        plt.savefig('/app/output/metric_correlations.png')
        plt.close()

    @staticmethod
    def plot_bleu_distribution(data: Dict[str, Dict[str, List[float]]]):
        plt.figure(figsize=(12, 6))
        all_bleu_scores = [score for translator in data.values() for score in translator.get('bleu_score', [])]
        
        sns.histplot(all_bleu_scores, kde=True)
        plt.title('Distribution of BLEU Scores')
        plt.xlabel('BLEU Score')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig('/app/output/bleu_distribution.png')
        plt.close()

    @staticmethod
    def plot_metric_comparison(data: Dict[str, Dict[str, List[float]]]):
        plt.figure(figsize=(12, 6))
        metrics = ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']
        
        for metric in metrics:
            all_scores = [score for translator in data.values() for score in translator.get(metric, [])]
            if all_scores:
                sns.kdeplot(all_scores, label=metric.upper())

        plt.title('Comparison of Metric Distributions')
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.legend()
        plt.tight_layout()
        plt.savefig('/app/output/metric_comparison.png')
        plt.close()

    @staticmethod
    def plot_bleu_score_comparison(records: List[Dict[str, Any]], score_type: str = 'bleu_score'):
        leaflet_data = defaultdict(lambda: {'best': None, 'highest': None, 'all': []})

        for record in records:
            leaflet_id = record.get('evaluation_leaflet_data', {}).get('leaflet_id')
            if leaflet_id is None:
                continue

            best_bleu = record.get('best_translation', {}).get('evaluation_scores', {}).get(score_type)
            if best_bleu is not None:
                leaflet_data[leaflet_id]['best'] = best_bleu

            all_bleu_scores = [t.get('evaluation_scores', {}).get(score_type) for t in record.get('translations', [])]
            all_bleu_scores = [score for score in all_bleu_scores if score is not None]
            
            if all_bleu_scores:
                leaflet_data[leaflet_id]['highest'] = max(all_bleu_scores)
                leaflet_data[leaflet_id]['all'].extend(all_bleu_scores)

        # Prepare data for plotting
        leaflets = list(leaflet_data.keys())
        best_scores = [data['best'] for data in leaflet_data.values()]
        highest_scores = [data['highest'] for data in leaflet_data.values()]

        # Create the plot
        plt.figure(figsize=(15, 8))
        bar_width = 0.35
        index = np.arange(len(leaflets))

        best_bars = plt.bar(index, best_scores, bar_width, label='Best Translation', alpha=0.8)
        highest_bars = plt.bar(index + bar_width, highest_scores, bar_width, label='Highest BLEU', alpha=0.8)

        # Add text labels on bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom')

        add_labels(best_bars)
        add_labels(highest_bars)

        # Plot individual translation scores
        for i, leaflet in enumerate(leaflets):
            all_scores = leaflet_data[leaflet]['all']
            plt.scatter([i + bar_width/2] * len(all_scores), all_scores, color='red', alpha=0.3, s=20, label='Individual Translations' if i == 0 else "")

        plt.xlabel('Leaflet ID')
        plt.ylabel('BLEU Score')
        plt.title('BLEU Score Comparison by Leaflet')
        plt.xticks(index + bar_width/2, leaflets, rotation=45)
        plt.legend()
        plt.tight_layout()

        plt.savefig('/app/output/bleu_score_comparison.png')
        plt.close()