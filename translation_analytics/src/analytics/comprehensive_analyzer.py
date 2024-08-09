from typing import List, Dict, Any
import numpy as np

class ComprehensiveAnalyzer:
    @staticmethod
    def generate_insights(processed_data: Dict[str, Any]) -> List[str]:
        insights = []

        # Translator Performance Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_translator_performance(processed_data['translator_performance']))

        # BLEU Score Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_bleu_scores(processed_data['translator_performance']))

        # Multi-Metric Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_multi_metrics(processed_data['translator_performance']))

        # Input Complexity Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_input_complexity(processed_data['input_complexity']))

        # Time Series Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_time_series(processed_data['time_series']))

        # Correlation Analysis
        insights.extend(ComprehensiveAnalyzer._analyze_correlations(processed_data['correlations']))

        return insights

    @staticmethod
    def _analyze_translator_performance(performance: Dict[str, Dict[str, List[float]]]) -> List[str]:
        insights = ["Translator Performance Analysis:"]
        for translator, metrics in performance.items():
            insights.append(f"\n  Translator: {translator}")
            for metric, scores in metrics.items():
                avg_score = np.mean(scores)
                insights.append(f"    Average {metric}: {avg_score:.4f}")
        return insights

    @staticmethod
    def _analyze_bleu_scores(performance: Dict[str, Dict[str, List[float]]]) -> List[str]:
        insights = ["\nBLEU Score Analysis:"]
        all_bleu_scores = [score for translator in performance.values() for score in translator.get('bleu_score', [])]
        avg_bleu = np.mean(all_bleu_scores)
        std_bleu = np.std(all_bleu_scores)
        insights.append(f"  Average BLEU score: {avg_bleu:.4f}")
        insights.append(f"  Standard deviation of BLEU scores: {std_bleu:.4f}")
        
        outliers = [score for score in all_bleu_scores if abs(score - avg_bleu) > 2 * std_bleu]
        insights.append(f"  Number of outlier BLEU scores: {len(outliers)}")
        if outliers:
            insights.append(f"  Range of outlier BLEU scores: {min(outliers):.4f} - {max(outliers):.4f}")
        return insights

    @staticmethod
    def _analyze_multi_metrics(performance: Dict[str, Dict[str, List[float]]]) -> List[str]:
        insights = ["\nMulti-Metric Analysis:"]
        metrics = ['bleu_score', 'comet_score', 'chrf_score', 'wer_score']
        for metric in metrics:
            all_scores = [score for translator in performance.values() for score in translator.get(metric, [])]
            if all_scores:
                avg_score = np.mean(all_scores)
                insights.append(f"  Average {metric}: {avg_score:.4f}")
        return insights

    @staticmethod
    def _analyze_input_complexity(complexity: Dict[int, Dict[str, List[float]]]) -> List[str]:
        insights = ["\nInput Complexity Analysis:"]
        for length, metrics in complexity.items():
            insights.append(f"\n  Input length: {length} words")
            for metric, scores in metrics.items():
                avg_score = np.mean(scores)
                insights.append(f"    Average {metric}: {avg_score:.4f}")
        return insights

    @staticmethod
    def _analyze_time_series(time_series: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        insights = ["\nTime Series Analysis:"]
        for metric, data in time_series.items():
            if data:
                scores = [item['score'] for item in data]
                start_score = scores[0]
                end_score = scores[-1]
                change = end_score - start_score
                insights.append(f"  {metric}:")
                insights.append(f"    Start: {start_score:.4f}, End: {end_score:.4f}")
                insights.append(f"    Overall change: {change:.4f}")
        return insights

    @staticmethod
    def _analyze_correlations(correlations: Dict[str, Dict[str, float]]) -> List[str]:
        insights = ["\nCorrelation Analysis:"]
        for metric1, corr_dict in correlations.items():
            for metric2, corr_value in corr_dict.items():
                insights.append(f"  Correlation between {metric1} and {metric2}: {corr_value:.4f}")
        return insights