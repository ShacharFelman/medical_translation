import os
from db.mongodb_client import MongoDBClient
from data.data_processor import DataProcessor
from analytics.translator_analyzer import TranslatorAnalyzer
from analytics.system_performance_analyzer import SystemPerformanceAnalyzer
from analytics.leaflet_analyzer import LeafletAnalyzer
from analytics.bleu_score_analyzer import BLEUScoreAnalyzer
from visualization.plot_generator import PlotGenerator

def main():
    # Initialize MongoDB client
    mongo_client = MongoDBClient()

    # Fetch all records
    all_records = mongo_client.get_all_records()

    # Process data
    translator_performance = DataProcessor.process_translator_performance(all_records)
    leaflet_performance = DataProcessor.process_leaflet_performance(all_records)
    bleu_data = DataProcessor.process_bleu_score_data(all_records)

    # Generate insights
    translator_insights = TranslatorAnalyzer.generate_insights(translator_performance)
    leaflet_insights = LeafletAnalyzer.generate_insights(leaflet_performance)
    bleu_insights = BLEUScoreAnalyzer.generate_insights(bleu_data)


    all_insights = (
        ["Translator Insights:"] + translator_insights +
        ["\nLeaflet Performance Insights:"] + leaflet_insights +
        ["\nBLEU Score Insights:"] + bleu_insights
    )

    # Print all insights
    print("\n".join(all_insights))

    # Save insights to a file
    with open('/app/output/translation_insights.txt', 'w') as f:
        f.write("\n".join(all_insights))

    # Generate plots
    PlotGenerator.plot_translator_performance(translator_performance, 'bleu')
    PlotGenerator.plot_translator_performance(translator_performance, 'comet')
    PlotGenerator.plot_translator_performance(translator_performance, 'response_time')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'bleu')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'comet')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'response_time')
    PlotGenerator.plot_bleu_insights(bleu_data)

if __name__ == "__main__":
    main()