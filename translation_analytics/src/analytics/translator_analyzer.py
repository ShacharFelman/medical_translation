from typing import List, Dict

class TranslatorAnalyzer:
    @staticmethod
    def generate_insights(translator_performance: Dict[str, Dict[str, float]]) -> List[str]:
        insights = []
        for translator, metrics in translator_performance.items():
            insights.append(f"Translator: {translator}")
            insights.append(f"  Average BLEU score: {metrics.get('bleu', 'N/A'):.4f}")
            insights.append(f"  Average COMET score: {metrics.get('comet', 'N/A'):.4f}")
            insights.append(f"  Average response time: {metrics.get('response_time', 'N/A'):.2f} seconds")
            insights.append(f"  Average similarity score: {metrics.get('score', 'N/A'):.4f}")
            insights.append("")
        return insights