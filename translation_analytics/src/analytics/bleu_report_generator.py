# File: analytics/bleu_report_generator.py

from typing import List, Dict, Any
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class BLEUReportGenerator:
    @staticmethod
    def generate_bleu_report(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        best_translation_report = BLEUReportGenerator._calculate_bleu_scores(records, use_best=True)
        highest_bleu_report = BLEUReportGenerator._calculate_bleu_scores(records, use_best=False)
        
        report = {
            "best_translation": best_translation_report,
            "highest_bleu": highest_bleu_report
        }

        BLEUReportGenerator._generate_bleu_comparison_plot(best_translation_report, highest_bleu_report)

        return report

    @staticmethod
    def _calculate_bleu_scores(records: List[Dict[str, Any]], use_best: bool) -> Dict[str, Any]:
        leaflet_scores = defaultdict(list)
        section_scores = defaultdict(list)

        for record in records:
            leaflet_id = record.get('evaluation_leaflet_data', {}).get('leaflet_id')
            section_number = record.get('evaluation_leaflet_data', {}).get('section_number')

            if use_best:
                bleu_score = record.get('best_translation', {}).get('evaluation_scores', {}).get('bleu_score')
            else:
                bleu_scores = [t.get('evaluation_scores', {}).get('bleu_score') for t in record.get('translations', [])]
                bleu_scores = [score for score in bleu_scores if score is not None]
                bleu_score = max(bleu_scores) if bleu_scores else None

            if bleu_score is not None:
                if leaflet_id is not None:
                    leaflet_scores[leaflet_id].append(bleu_score)
                if section_number is not None:
                    section_scores[section_number].append(bleu_score)

        avg_leaflet_scores = {
            leaflet_id: sum(scores) / len(scores)
            for leaflet_id, scores in leaflet_scores.items()
        }

        avg_section_scores = {
            section_number: sum(scores) / len(scores)
            for section_number, scores in section_scores.items()
        }

        all_scores = [score for scores in leaflet_scores.values() for score in scores]
        overall_avg = sum(all_scores) / len(all_scores) if all_scores else None

        return {
            "avg_leaflet_scores": avg_leaflet_scores,
            "avg_section_scores": avg_section_scores,
            "overall_avg": overall_avg
        }

    @staticmethod
    def _generate_bleu_comparison_plot(best_translation_report: Dict[str, Any], highest_bleu_report: Dict[str, Any]):
        leaflets = list(best_translation_report['avg_leaflet_scores'].keys())
        best_scores = [best_translation_report['avg_leaflet_scores'][leaflet] for leaflet in leaflets]
        highest_scores = [highest_bleu_report['avg_leaflet_scores'][leaflet] for leaflet in leaflets]

        plt.figure(figsize=(15, 8))
        bar_width = 0.35
        index = np.arange(len(leaflets))

        best_bars = plt.bar(index, best_scores, bar_width, label='Best Translation', alpha=0.8)
        highest_bars = plt.bar(index + bar_width, highest_scores, bar_width, label='Highest BLEU', alpha=0.8)

        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.2f}',
                         ha='center', va='bottom')

        add_labels(best_bars)
        add_labels(highest_bars)

        plt.xlabel('Leaflet ID')
        plt.ylabel('Average BLEU Score')
        plt.title('BLEU Score Comparison by Leaflet')
        plt.xticks(index + bar_width/2, leaflets, rotation=45)
        plt.legend()
        plt.tight_layout()

        plt.savefig('/app/output/bleu_score_comparison.png')
        plt.close()

    @staticmethod
    def format_report(report: Dict[str, Any]) -> str:
        formatted_report = "BLEU Score Report\n==================\n\n"

        for report_type, data in report.items():
            formatted_report += f"{report_type.replace('_', ' ').title()}:\n"
            formatted_report += "-" * (len(report_type) + 1) + "\n"

            formatted_report += "Average BLEU score per leaflet:\n"
            for leaflet_id, score in data['avg_leaflet_scores'].items():
                formatted_report += f"  Leaflet {leaflet_id}: {score:.4f}\n"

            formatted_report += "\nAverage BLEU score per section:\n"
            for section_number, score in data['avg_section_scores'].items():
                formatted_report += f"  Section {section_number}: {score:.4f}\n"

            if data['overall_avg'] is not None:
                formatted_report += f"\nOverall average BLEU score: {data['overall_avg']:.4f}\n\n"
            else:
                formatted_report += "\nOverall average BLEU score: N/A\n\n"

        return formatted_report