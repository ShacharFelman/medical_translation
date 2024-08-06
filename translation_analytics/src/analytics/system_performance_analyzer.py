from typing import List, Dict, Any

class SystemPerformanceAnalyzer:
    @staticmethod
    def generate_insights(processed_data: List[Dict[str, Any]]) -> List[str]:
        if not processed_data:
            return ["No data available for system performance insights."]

        latest = processed_data[-1]
        earliest = processed_data[0]
        total_duration = (latest['timestamp'] - earliest['timestamp']).days

        avg_bleu = sum(r['bleu'] for r in processed_data if r['bleu']) / len([r for r in processed_data if r['bleu']])
        avg_comet = sum(r['comet'] for r in processed_data if r['comet']) / len([r for r in processed_data if r['comet']])
        avg_response_time = sum(r['response_time'] for r in processed_data) / len(processed_data)

        insights = [
            f"System Performance over {total_duration} days:",
            f"  Average BLEU score: {avg_bleu:.4f}",
            f"  Average COMET score: {avg_comet:.4f}",
            f"  Average response time: {avg_response_time:.2f} seconds",
            "",
            f"Latest performance metrics (as of {latest['timestamp']}):",
            f"  BLEU score: {latest['bleu']:.4f}",
            f"  COMET score: {latest['comet']:.4f}",
            f"  Response time: {latest['response_time']:.2f} seconds"
        ]
        return insights