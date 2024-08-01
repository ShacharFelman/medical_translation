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
    def plot_system_performance_over_time(data: List[Dict[str, Any]], metric: str):
        timestamps = [d['timestamp'] for d in data]
        values = [d.get(metric, 0) for d in data]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, values)
        plt.title(f'System Performance Over Time - {metric.capitalize()}')
        plt.xlabel('Timestamp')
        plt.ylabel(metric.capitalize())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'/app/output/system_performance_{metric}.png')
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