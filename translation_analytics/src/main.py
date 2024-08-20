# File: src/main.py

import os
from db.mongodb_client import MongoDBClient
from data.data_processor import DataProcessor
from analytics.comprehensive_analyzer import ComprehensiveAnalyzer
from analytics.bleu_report_generator import BLEUReportGenerator
from visualization.plot_generator import PlotGenerator

def main():
    # Initialize MongoDB client
    mongo_client = MongoDBClient()

    # Fetch all records
    all_records = mongo_client.get_all_records()

    # # Process data
    # translator_performance = DataProcessor.process_translator_performance(all_records)
    # input_complexity = DataProcessor.process_input_complexity(all_records)
    # time_series_data = DataProcessor.process_time_series_data(all_records)
    
    # # Calculate correlations
    # all_scores = []
    # for translator, metrics in translator_performance.items():
    #     for metric, scores in metrics.items():
    #         all_scores.extend([{metric: score} for score in scores])

    # correlations = DataProcessor.calculate_correlations(all_scores)

    # Prepare data for comprehensive analysis
    # analysis_data = {
    #     'translator_performance': translator_performance,
    #     'input_complexity': input_complexity,
    #     'time_series': time_series_data,
    #     'correlations': correlations
    # }

    # # Generate comprehensive insights
    # comprehensive_insights = ComprehensiveAnalyzer.generate_insights(analysis_data)

    # # Print all insights
    # print("\n".join(comprehensive_insights))

    # # Save insights to a file
    # with open('/app/output/comprehensive_translation_insights.txt', 'w') as f:
    #     f.write("\n".join(comprehensive_insights))

    # Generate plots
    # metrics = ['bleu_score', 'comet_score', 'chrf_score', 'wer_score', 'response_time']
    # for metric in metrics:
    #     PlotGenerator.plot_translator_performance(translator_performance, metric)
    
    # PlotGenerator.plot_input_complexity(input_complexity)
    # PlotGenerator.plot_time_series(time_series_data)
    # PlotGenerator.plot_correlations(correlations)
    # PlotGenerator.plot_bleu_distribution(translator_performance)
    # PlotGenerator.plot_metric_comparison(translator_performance)

    # Generate BLEU score report and comparison plot
    bleu_report = BLEUReportGenerator.generate_bleu_report(all_records)
    # formatted_report = BLEUReportGenerator.format_report(bleu_report)

    # Save BLEU score report to a file
    # with open('/app/output/bleu_score_report.txt', 'w') as f:
    #     f.write(formatted_report)

    # print("BLEU score report generated and saved to '/app/output/bleu_score_report.txt'")
    print("BLEU score comparison plot generated and saved to '/app/output/bleu_score_comparison.png'")

if __name__ == "__main__":
    main()