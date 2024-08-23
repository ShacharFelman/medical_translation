from typing import List, Dict, Any
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from utils.constants import BLEUScoreType
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, TranslationEntity
from matplotlib.colors import LinearSegmentedColormap


mongo_client = MongoDBClient()


def generate_bleu_report(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    best_translation_report = {}

    try:
        best_translation_report = calculate_bleu_scores(records)
        generate_bleu_leaflet_comparison_plot(best_translation_report)
        generate_bleu_section_comparison_plot(best_translation_report)

    except Exception as e:
        print(f"Error processing BLEU : {str(e)}")

    return best_translation_report

def calculate_bleu_scores(records: List[TranslationRecordEntity]) -> Dict[str, Any]:
    leaflet_scores = defaultdict(list)
    section_scores = defaultdict(list)

    for record in records:
        bleu_score = get_bleu_score(record.best_translation)
        if bleu_score is not None:
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
        scores = [bleu.get(bleu_type, None) for bleu_type in BLEUScoreType.get_types_tokenized()]
        scores = [score for score in scores if score is not None]
        if not scores or len(scores) == 0:
            return bleu.get(BLEUScoreType.PLAIN_CORPUS.value, None)
        bleu_score = max(scores)
        return bleu_score
    
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

    fig, ax = plt.subplots(figsize=(15, 8))
    bar_width = 0.6
    index = np.arange(len(leaflets))

    # Define colors for bars above and below threshold
    above_color = '#5E48C0'     # Dark purple
    below_color = '#8D71D2'     # Light purple
    threshold = 0.6

    # Create custom colormap for background
    colors = ['red', 'yellow', 'green']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # # Create vertical background color scale with 20% opacity and inverted colors
    # background = ax.imshow([[1 - i/n_bins] for i in range(n_bins)], cmap=cmap, aspect='auto', 
    #                        extent=[-0.5, len(leaflets)-0.5, 0, 0.8], alpha=0.1)

    # Create bars with colors based on threshold, centered on tick marks
    best_bars = ax.bar(index, best_scores, bar_width, 
                       color=[above_color if score >= threshold else below_color for score in best_scores],
                       alpha=0.8)

    add_bar_labels(best_bars)

    ax.set_xlabel('Leaflet ID')
    ax.set_ylabel('Average BLEU Score')
    ax.set_title('BLEU Score Comparison by Leaflet')
    ax.set_xticks(index)
    ax.set_xticklabels(leaflets, rotation=45, ha='right')
    
    ax.set_ylim(0, 0.8)
    
    # Add threshold line
    ax.axhline(y=threshold, color='black', linestyle='--', label=f'Threshold ({threshold})', )
    
    # Create legend
    ax.legend([plt.Rectangle((0,0),1,1,fc=above_color, alpha=0.8),
               plt.Rectangle((0,0),1,1,fc=below_color, alpha=0.8),
               plt.Line2D([0], [0], color='black', linestyle='--')],
              ['Above Threshold', 'Below Threshold', f'Threshold ({threshold})'])
    
    # Add color scale
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', aspect=30, pad=0.02)
    cbar.set_label('BLEU Score Scale')
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
    cbar.set_ticklabels(['0', '20', '40', '60', '≥80'])

    plt.tight_layout()

    output_path = save_plot('bleu_leaflets_scores')
    print(f"Plot saved successfully: {output_path}")

def generate_bleu_section_comparison_plot(best_translation_report: Dict[str, Any]):
    sections = list(best_translation_report['avg_section_scores'].keys())
    best_scores = [best_translation_report['avg_section_scores'][section] for section in sections]

    fig, ax = plt.subplots(figsize=(15, 8))
    bar_width = 0.6
    index = np.arange(len(sections))

    # Define colors for bars above and below threshold
    above_color = '#5E48C0'     # Dark purple
    below_color = '#8D71D2'     # Light purple
    threshold = 0.6

    # Create custom colormap for background
    colors = ['red', 'yellow', 'green']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # Create bars with colors based on threshold, centered on tick marks
    best_bars = ax.bar(index, best_scores, bar_width, 
                       color=[above_color if score >= threshold else below_color for score in best_scores],
                       alpha=0.8)

    add_bar_labels(best_bars)

    ax.set_xlabel('Section Number')
    ax.set_ylabel('Average BLEU Score')
    ax.set_title('BLEU Score Comparison by Section')
    ax.set_xticks(index)
    ax.set_xticklabels(sections, rotation=45, ha='right')
    
    ax.set_ylim(0, 0.8)
    
    # Add threshold line
    ax.axhline(y=threshold, color='black', linestyle='--', label=f'Threshold ({threshold})')
    
    # Create legend
    ax.legend([plt.Rectangle((0,0),1,1,fc=above_color, alpha=0.8),
               plt.Rectangle((0,0),1,1,fc=below_color, alpha=0.8),
               plt.Line2D([0], [0], color='black', linestyle='--')],
              ['Above Threshold', 'Below Threshold', f'Threshold ({threshold})'])
    
    # Add color scale
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', aspect=30, pad=0.02)
    cbar.set_label('BLEU Score Scale')
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
    cbar.set_ticklabels(['0', '20', '40', '60', '≥80'])

    plt.tight_layout()

    output_path = save_plot('bleu_sections_scores')
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