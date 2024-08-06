from typing import List, Dict, Any

class BLEUScoreAnalyzer:
    @staticmethod
    def generate_insights(processed_data: Dict[str, Any]) -> List[str]:
        insights = []

        # Translator Performance Insight
        translator_performance = processed_data['translator_performance']
        best_translator = max(translator_performance, key=translator_performance.get)
        worst_translator = min(translator_performance, key=translator_performance.get)
        insights.append(f"Best performing translator (BLEU): {best_translator} (Avg BLEU: {translator_performance[best_translator]:.4f})")
        insights.append(f"Worst performing translator (BLEU): {worst_translator} (Avg BLEU: {translator_performance[worst_translator]:.4f})")

        # Input Complexity Insight
        input_complexity = processed_data['input_complexity']
        avg_bleu_by_length = sum(input_complexity.values()) / len(input_complexity)
        insights.append(f"Average BLEU score across all input lengths: {avg_bleu_by_length:.4f}")
        if input_complexity:
            worst_length = min(input_complexity, key=input_complexity.get)
            insights.append(f"Input length with lowest average BLEU score: {worst_length} words (Avg BLEU: {input_complexity[worst_length]:.4f})")

        # Metric Correlation Insight
        metric_correlation = processed_data['metric_correlation']
        if metric_correlation:
            avg_bleu = sum(item['bleu_score'] for item in metric_correlation if item['bleu_score']) / len(metric_correlation)
            avg_comet = sum(item['comet_score'] for item in metric_correlation if item['comet_score']) / len(metric_correlation)
            insights.append(f"Average BLEU score: {avg_bleu:.4f}, Average COMET score: {avg_comet:.4f}")

        return insights