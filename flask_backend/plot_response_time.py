from typing import List, Dict, Union
from collections import defaultdict
import matplotlib.pyplot as plt
from pathlib import Path
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity
import matplotlib.pyplot as plt
from collections import Counter

mongo_client = MongoDBClient()

def calculate_average_scores(scores: Dict[str, List[float]]) -> Dict[str, float]:
    return {key: sum(values) / len(values) for key, values in scores.items()}

def get_record_response_time(record: TranslationRecordEntity) -> float:
    return max(translation.response_time for translation in record.translations)

def calculate_response_time_by_leaflet(records: List[TranslationRecordEntity]) -> Dict[str, float]:
    leaflet_response_times = defaultdict(float)
    
    for record in records:
        leaflet_id = record.evaluation_leaflet_data.leaflet_id
        leaflet_response_times[leaflet_id] += get_record_response_time(record)/60
    
    return dict(leaflet_response_times)

def calculate_response_time_by_model(records: List[TranslationRecordEntity]) -> Dict[str, float]:
    model_response_times = defaultdict(list)
    
    for record in records:
        for translation in record.translations:
            model_response_times[translation.translator_name].append(translation.response_time)
    
    return {model: sum(times) / len(times) for model, times in model_response_times.items()}

def calculate_average_response_time_per_record(records: List[TranslationRecordEntity]) -> float:
    total_response_time = sum(get_record_response_time(record) for record in records)
    return total_response_time / len(records)

def calculate_leaflet_sizes(records: List[TranslationRecordEntity]) -> Dict[str, int]:
    leaflet_sizes = Counter()
    
    for record in records:
        leaflet_id = str(record.evaluation_leaflet_data.leaflet_id)
        leaflet_sizes[leaflet_id] += 1
    
    return dict(leaflet_sizes)

def generate_response_time_plot(data: Union[Dict[str, float], float], plot_type: str):
    fig, ax = plt.subplots(figsize=(20, 10))  # Increased figure size
    
    if isinstance(data, dict):
        labels = list(data.keys())
        values = list(data.values())
        
        # Sort data by values in descending order
        sorted_data = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
        labels, values = zip(*sorted_data)
        
        x = range(len(labels))
        bars = ax.bar(x, values, color='#5E48C0', width=0.8)  # Increased bar width
        
        ax.set_xlabel('ID' if plot_type != 'models' else 'Model', fontsize=12)
        ax.set_ylabel('Average Response Time (seconds)', fontsize=12)
        ax.set_title(f'Average Response Time per {plot_type.capitalize()}', fontsize=14)
        
        # Set x-axis ticks and labels
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=90, ha='center', fontsize=8)  # Vertical labels
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=8)
        
        # Add gridlines for better readability
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
    else:  # single float value
        bars = ax.bar(['Average'], [data], color='#5E48C0', width=0.4)
        ax.set_ylabel('Average Response Time (seconds)', fontsize=12)
        ax.set_title(f'Average Response Time per {plot_type.capitalize()}', fontsize=14)
        
        # Add value label on top of the bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    save_plot(f'response_time_{plot_type}')
    plt.close()

def generate_response_time_plot_size(data: Union[Dict[str, float], float], leaflet_sizes: Dict[str, int], plot_type: str):
    fig, ax = plt.subplots(figsize=(6, 7))  # Increased figure size
    
    if isinstance(data, dict):
        labels = list(data.keys())
        values = list(data.values())
        
        # Sort data by values in descending order
        sorted_data = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
        
        # Select 5 items from the middle
        middle_index = len(sorted_data) // 2
        start_index = middle_index - 2
        end_index = middle_index + 3
        selected_data = sorted_data[start_index:end_index]
        
        labels, values = zip(*selected_data)
        
        x = range(len(labels))
        bars = ax.bar(x, values, color='#5E48C0', width=0.3)  # Increased bar width
        
        ax.set_xlabel('ID' if plot_type != 'models' else 'Model', fontsize=12)
        ax.set_ylabel('Average Response Time (minutes)', fontsize=12)
        ax.set_title(f'Average Response Time for 5 Selected {plot_type.capitalize()}', fontsize=14)
        
        # Set x-axis ticks and labels
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)  # Angled labels for better readability
        
        ax.set_ylim(0, 10)

        # Add value labels on top of each bar
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f} min',
                    ha='center', va='bottom', fontsize=10)
        
        # Add gridlines for better readability
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
    else:  # single float value
        bars = ax.bar(['Average'], [data], color='#5E48C0', width=0.4)
        ax.set_ylabel('Average Response Time (minutes)', fontsize=12)
        ax.set_title(f'Average Response Time per {plot_type.capitalize()}', fontsize=14)

        ax.set_ylim(0, 10)

        # Add value label on top of the bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    save_plot(f'response_time_{plot_type}_5_selected')
    plt.close()

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
      
        # Generate response time plots
        leaflet_response_times = calculate_response_time_by_leaflet(all_records)
        model_response_times = calculate_response_time_by_model(all_records)
        average_response_time = calculate_average_response_time_per_record(all_records)

        leaflet_sizes = calculate_leaflet_sizes(all_records)

        generate_response_time_plot_size(leaflet_response_times, leaflet_sizes, 'leaflet')



        # generate_response_time_plot(leaflet_response_times, 'leaflet')
        generate_response_time_plot(model_response_times, 'models')
        generate_response_time_plot(average_response_time, 'average')

        print("Report and response time plots generation completed successfully.")
        project_dir = Path(__file__).resolve().parent.parent
        output_dir = project_dir / 'tests_output'
        print(f"Output files are saved in: {output_dir}")

    except Exception as e:
        print(f"An error occurred in the main execution: {str(e)}")

if __name__ == "__main__":
    main()