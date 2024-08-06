from typing import List, Dict

class LeafletAnalyzer:
    @staticmethod
    def generate_insights(processed_data: Dict[str, Dict[str, float]]) -> List[str]:
        insights = []
        for leaflet, metrics in processed_data.items():
            insights.append(f"Leaflet ID: {leaflet}")
            insights.append(f"  Average BLEU score: {metrics.get('bleu', 'N/A'):.4f}")
            insights.append(f"  Average COMET score: {metrics.get('comet', 'N/A'):.4f}")
            insights.append(f"  Average response time: {metrics.get('response_time', 'N/A'):.2f} seconds")
            insights.append("")
        return insights