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
    try:
        # scores_by_leaflet = calculate_bleu_scores_by_leaflets(records)
        # generate_bleu_comparison_plot(translation_report=scores_by_leaflet,
        #                               comparison_type='leaflets',
        #                               treshold=0.6,
        #                               fig_width=15,
        #                               fig_height=8,
        #                               bar_width=0.6,
        #                               x_label='Leaflet ID',
        #                               y_label='Average BLEU Score')
        
        # scores_by_sections = calculate_bleu_scores_by_sections(records)
        # generate_bleu_comparison_plot(translation_report=scores_by_sections,
        #                               comparison_type='sections',
        #                               treshold=0.6,
        #                               fig_width=12,
        #                               fig_height=8,
        #                               bar_width=0.5,
        #                               x_label='Section ID',
        #                               y_label='Average BLEU Score')
        
        scores_by_model = calculate_bleu_scores_by_model(records)
        generate_bleu_comparison_plot(translation_report=scores_by_model,
                                      comparison_type='models',
                                      treshold=0.6,
                                      fig_width=6,
                                      fig_height=7,
                                      bar_width=0.3,
                                      x_label='Model name',
                                      y_label='Average BLEU Score')
        
        # scores_best_actual_leaflets = calculate_bleu_scores_actual_best_leaflets(records)
        # scores_best_actual_sections = calculate_bleu_scores_actual_best_sections(records)
        # scores_best_actual_overall  = calculate_bleu_scores_actual_best_overall(records)
       
        # generate_comparison_plot_best_actual(scores_best_actual_leaflets, 'leaflets')
        # generate_comparison_plot_best_actual(scores_best_actual_sections, 'sections')
        # generate_comparison_plot_best_actual(scores_best_actual_overall, 'overall')


    except Exception as e:
        print(f"Error processing BLEU : {str(e)}")

    return True

def calculate_bleu_scores_by_leaflets(records: List[TranslationRecordEntity]) -> Dict[str, Any]:
    leaflet_scores = defaultdict(list)

    for record in records:
        bleu_score = get_bleu_score(record.best_translation)
        if bleu_score is not None:
            leaflet_id = record.evaluation_leaflet_data.leaflet_id
            if leaflet_id is not None:
                leaflet_scores[leaflet_id].append(bleu_score)

    avg_leaflet_scores = calculate_average_scores(leaflet_scores)

    print_scores(avg_leaflet_scores, "Leaflet", "Leaflet ID")

    return avg_leaflet_scores

def calculate_bleu_scores_by_sections(records: List[TranslationRecordEntity]) -> Dict[str, Any]:
    section_scores = defaultdict(list)

    for record in records:
        bleu_score = get_bleu_score(record.best_translation)
        if bleu_score is not None:
            section_number = record.evaluation_leaflet_data.section_number
            if section_number is not None:
                section_scores[section_number].append(bleu_score)

    avg_section_scores = calculate_average_scores(section_scores)

    print_scores(avg_section_scores, "Section")

    return avg_section_scores

def calculate_bleu_scores_by_model(records: List[TranslationRecordEntity]) -> Dict[str, Any]:
    models_scores = defaultdict(list)

    for record in records:
        for translation in record.translations:
            bleu_score = get_bleu_score(translation, 7)
            if bleu_score is not None:
                models_scores[translation.translator_name].append(bleu_score)

        best_bleu_score = None
        for translation in record.translations:
            bleu_score = get_bleu_score(translation)
            if bleu_score is not None:
                if best_bleu_score is None or bleu_score > best_bleu_score:
                    best_bleu_score = bleu_score

        if best_bleu_score is not None:
            models_scores["MediTranslate AI"].append(best_bleu_score)

    models_scores = calculate_average_scores(models_scores)

    print_scores(models_scores, "Model")

    return models_scores

def calculate_bleu_scores_actual_best_leaflets(records: List[TranslationRecordEntity]) -> Dict[str, Dict[str, float]]:
    best_translation_scores = defaultdict(list)
    actual_best_scores = defaultdict(list)

    for record in records:
        best_translation_score = get_bleu_score(record.best_translation)
        translation_scores = [get_bleu_score(translation) for translation in record.translations]
        translation_scores = [score for score in translation_scores if score is not None]
        actual_best_score = max(translation_scores) if translation_scores else None

        leaflet_id = record.evaluation_leaflet_data.leaflet_id

        best_translation_scores[leaflet_id].append(best_translation_score)
        actual_best_scores[leaflet_id].append(actual_best_score)

    return {
        'best_translation': calculate_average_scores(best_translation_scores),
        'actual_best': calculate_average_scores(actual_best_scores)
    }


def calculate_bleu_scores_actual_best_sections(records: List[TranslationRecordEntity]) -> Dict[str, Dict[str, float]]:
    best_translation_scores = defaultdict(list)
    actual_best_scores = defaultdict(list)

    for record in records:
        best_translation_score = get_bleu_score(record.best_translation)
        translation_scores = [get_bleu_score(translation) for translation in record.translations]
        translation_scores = [score for score in translation_scores if score is not None]
        actual_best_score = max(translation_scores) if translation_scores else None

        section_number = record.evaluation_leaflet_data.section_number

        best_translation_scores[section_number].append(best_translation_score)
        actual_best_scores[section_number].append(actual_best_score)

    return {
        'best_translation': calculate_average_scores(best_translation_scores),
        'actual_best': calculate_average_scores(actual_best_scores)
    }

def calculate_bleu_scores_actual_best_overall(records: List[TranslationRecordEntity]) -> Dict[str, Dict[str, float]]:
    best_translation_scores = defaultdict(list)
    actual_best_scores = defaultdict(list)

    for record in records:
        best_translation_score = get_bleu_score(record.best_translation)
        translation_scores = [get_bleu_score(translation) for translation in record.translations]
        translation_scores = [score for score in translation_scores if score is not None]
        actual_best_score = max(translation_scores) if translation_scores else None

        best_translation_scores['overall'].append(best_translation_score)
        actual_best_scores['overall'].append(actual_best_score)

    return {
        'best_translation': calculate_average_scores(best_translation_scores),
        'actual_best': calculate_average_scores(actual_best_scores)
    }

def get_bleu_score(translation: TranslationEntity, len_treshold_for_plain_corpus = 0) -> float:
    translation_len = len(translation.translated_text.split())

    if not translation or not translation.evaluation_scores:
        return None
    
    bleu = translation.evaluation_scores.get('bleu')
    if bleu:
        scores = [bleu.get(bleu_type, None) for bleu_type in BLEUScoreType.get_types_tokenized()]
        scores = [score for score in scores if score is not None]
        if not scores or len(scores) == 0 or translation_len < len_treshold_for_plain_corpus:
            return bleu.get(BLEUScoreType.PLAIN_CORPUS.value, None)
        bleu_score = max(scores)
        return bleu_score
    
    return None

def calculate_average_scores(scores: Dict[str, List[float]]) -> Dict[str, float]:
    return {key: sum(values) / len(values) for key, values in scores.items()}

def print_scores(avg_scores: Dict[str, float], comparison_type: str):
    print(f"========== BLEU Scores by {comparison_type} ==========")
    for id, score in avg_scores.items():
        print(f'{comparison_type} ID: {id}, BLEU Score: {score}')

def generate_bleu_comparison_plot(translation_report: Dict[str, Any],
                                  comparison_type: str,
                                  treshold: float,
                                  fig_height: int,
                                  fig_width: int,
                                  bar_width: float,
                                  x_label: str,
                                  y_label: str):
    
    x_values = list(translation_report.keys())
    y_values = [translation_report[x] for x in x_values]

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    index = np.arange(len(x_values))

    # Define colors for bars above and below threshold
    above_color = '#5E48C0'     # Dark purple
    below_color = '#8D71D2'     # Light purple
    threshold = treshold

    # Create custom colormap for background
    colors = ['red', 'yellow', 'green']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # Create bars with colors based on threshold, centered on tick marks
    best_bars = ax.bar(index, y_values, bar_width, 
                       color=[above_color if y >= threshold else below_color for y in y_values],
                       alpha=0.8)

    add_bar_labels(best_bars)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f'BLEU Score Comparison by {comparison_type}')
    ax.set_xticks(index)
    ax.set_xticklabels(x_values, rotation=45, ha='right')
    
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

    output_path = save_plot(f'bleu_{comparison_type}_scores')
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


def generate_comparison_plot_best_actual(data: Dict[str, Dict[str, float]], plot_type: str, threshold: float = 0.6):
    labels = list(set(data['best_translation'].keys()) | set(data['actual_best'].keys()))
    best_translation_scores = [data['best_translation'].get(label, 0) for label in labels]
    actual_best_scores = [data['actual_best'].get(label, 0) for label in labels]

    fig, ax = plt.subplots(figsize=(15, 8))
    index = np.arange(len(labels))
    bar_width = 0.35

    # Define colors for bars
    best_translation_color = '#8D71D2'  # Light purple
    actual_best_color = '#5E48C0'  # Dark purple

    # Create custom colormap for background
    colors = ['red', 'yellow', 'green']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # Create bars
    best_bars = ax.bar(index - bar_width/2, best_translation_scores, bar_width,
                       color=best_translation_color, alpha=0.8, label='Best Translation')
    actual_bars = ax.bar(index + bar_width/2, actual_best_scores, bar_width,
                         color=actual_best_color, alpha=0.8, label='Actual Best')

    add_bar_labels(best_bars)
    add_bar_labels(actual_bars)

    ax.set_xlabel('ID' if plot_type != 'overall' else '')
    ax.set_ylabel('Average BLEU Score')
    ax.set_title(f'BLEU Score Comparison by {plot_type.capitalize()}')
    ax.set_xticks(index)
    ax.set_xticklabels(labels, rotation=45, ha='right')

    ax.set_ylim(0, 0.9)

    # Create legend
    ax.legend([plt.Rectangle((0,0),1,1,fc=best_translation_color, alpha=0.8),
               plt.Rectangle((0,0),1,1,fc=actual_best_color, alpha=0.8)],
              ['Best Translation', 'Actual Best'])

    # Add color scale
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', aspect=30, pad=0.02)
    cbar.set_label('BLEU Score Scale')
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
    cbar.set_ticklabels(['0', '20', '40', '60', '≥80'])

    plt.tight_layout()
    save_plot(f'bleu_{plot_type}_comparison_best_actual')
    plt.close()


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