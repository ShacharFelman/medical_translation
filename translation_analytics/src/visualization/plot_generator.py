import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
import numpy as np
from datetime import datetime

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