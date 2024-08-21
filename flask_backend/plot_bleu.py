from typing import List, Dict, Any
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from utils.constants import BLEUScoreType
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, TranslationEntity

mongo_client = MongoDBClient()
len_threshold = 10
score_threshold = 0.00


def generate_bleu_report(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    best_translation_report = {}

    try:
        best_translation_report = calculate_bleu_scores(records)
        generate_bleu_leaflet_comparison_plot(best_translation_report)
    except Exception as e:
        print(f"Error processing BLEU : {str(e)}")

    return best_translation_report

def calculate_bleu_scores(records: List[TranslationRecordEntity]) -> Dict[str, Any]:
    leaflet_scores = defaultdict(list)
    section_scores = defaultdict(list)

    bleu_scores = []
    for record in records:
        bleu_scores = [get_bleu_score(translation) for translation in record.translations]
        bleu_scores.append(get_bleu_score(record.best_translation))
        bleu_scores = [score for score in bleu_scores if score is not None]
        bleu_score = max(bleu_scores)
        if bleu_score is not None:
            if bleu_score < score_threshold:
                print(f"{record.evaluation_leaflet_data.leaflet_id}, {record.evaluation_leaflet_data.section_number}[{record.evaluation_leaflet_data.array_location}]. Low BLEU score found: {bleu_score}")
            update_scores(record, bleu_score, leaflet_scores, section_scores)

    avg_leaflet_scores = calculate_average_scores(leaflet_scores)
    avg_section_scores = calculate_average_scores(section_scores)
    overall_avg = calculate_overall_average(leaflet_scores)

    print_leaflet_scores(avg_leaflet_scores)
    print_section_scores(avg_section_scores)
    print_overall_scores(overall_avg)

    return {
        "avg_leaflet_scores": avg_leaflet_scores,
        "avg_section_scores": avg_section_scores,
        "overall_avg": overall_avg
    }

def get_bleu_score(translation: TranslationEntity) -> float:
    if not translation or not translation.evaluation_scores:
        return None
    
    bleu = translation.evaluation_scores.get('bleu')
    if bleu:
        if len(translation.translated_text) > len_threshold:
            scores = [bleu.get(bleu_type, None) for bleu_type in BLEUScoreType.get_types_tokenized()]
            scores = [score for score in scores if score is not None]
            if not scores or len(scores) == 0:
                return bleu.get(BLEUScoreType.PLAIN_CORPUS.value, None)
            bleu_score = max(scores)
            if bleu_score > score_threshold:
                return bleu_score
            else:
                return bleu.get(BLEUScoreType.PLAIN_CORPUS.value, None)
        else:
            return bleu.get(BLEUScoreType.PLAIN_CORPUS.value, None)
    return None

def update_scores(record: TranslationRecordEntity, bleu_score: float, leaflet_scores: Dict[str, List[float]], section_scores: Dict[str, List[float]]):
    leaflet_id = record.evaluation_leaflet_data.leaflet_id
    section_number = record.evaluation_leaflet_data.section_number

    if leaflet_id is not None:
        leaflet_scores[leaflet_id].append(bleu_score)
    if section_number is not None:
        section_scores[section_number].append(bleu_score)

def calculate_average_scores(scores: Dict[str, List[float]]) -> Dict[str, float]:
    return {key: sum(values) / len(values) for key, values in scores.items()}

def calculate_overall_average(scores: Dict[str, List[float]]) -> float:
    all_scores = [score for scores_list in scores.values() for score in scores_list]
    return sum(all_scores) / len(all_scores) if all_scores else None

def print_leaflet_scores(avg_scores: Dict[str, float]):
    print("========== BLEU Scores by Leaflet ==========")
    for leaflet_id, avg_score in avg_scores.items():
        print(f'Leaflet ID: {leaflet_id}, BLEU Score: {avg_score}')

def print_section_scores(avg_scores: Dict[str, float]):
    print("========== BLEU Scores by Section ==========")
    for section_id, avg_score in avg_scores.items():
        print(f'Section ID: {section_id}, BLEU Score: {avg_score}')

def print_overall_scores(avg_score: float):
    print("========== Overall BLEU Score ==========")
    print(f'Overall BLEU Score: {avg_score}')

def generate_bleu_leaflet_comparison_plot(best_translation_report: Dict[str, Any]):
    leaflets = list(best_translation_report['avg_leaflet_scores'].keys())
    best_scores = [best_translation_report['avg_leaflet_scores'][leaflet] for leaflet in leaflets]

    plt.figure(figsize=(15, 8))
    bar_width = 0.35
    index = np.arange(len(leaflets))

    best_bars = plt.bar(index, best_scores, bar_width, label='Best Translation', alpha=0.8)

    add_bar_labels(best_bars)

    plt.xlabel('Leaflet ID')
    plt.ylabel('Average BLEU Score')
    plt.title(f'BLEU Score Comparison by Leaflet with length threshold of {len_threshold}')
    plt.xticks(index + bar_width/2, leaflets, rotation=45)
    plt.legend()
    
    plt.ylim(0, 0.8)
    
    plt.tight_layout()

    output_path = save_plot('bleu_leaflets_scores')
    print(f"Plot saved successfully: {output_path}")

def add_bar_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')

def save_plot(score_type: str) -> Path:
    project_dir = Path(__file__).resolve().parent.parent
    output_dir = project_dir / 'tests_output'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{score_type}_comparison.png'
    plt.savefig(output_path)
    plt.close()
    return output_path

def main():
    try:
        all_records = mongo_client.get_all_translation_records()

        if not all_records:
            print("No records found in the database.")
            return

        print(f"Retrieved {len(all_records)} records from the database.")

        best_report = generate_bleu_report(all_records)
        
        if best_report:
            print("BLEU report generation completed successfully.")
            project_dir = Path(__file__).resolve().parent.parent
            output_dir = project_dir / 'tests_output'
            print(f"Output files are saved in: {output_dir}")
        else:
            print("BLEU report generation failed or produced empty reports.")
    except Exception as e:
        print(f"An error occurred in the main execution: {str(e)}")

if __name__ == "__main__":
    main()