import os
from db.mongodb_client import MongoDBClient
from data.data_processor import DataProcessor
from analytics.analytics_generator import AnalyticsGenerator
from visualization.plot_generator import PlotGenerator

def main():
    # Initialize MongoDB client
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
    mongo_db = os.getenv('MONGO_DB', 'translation_db')
    mongo_client = MongoDBClient(mongo_uri, mongo_db)

    # Fetch all records
    all_records = mongo_client.get_all_records()

    # Process data
    translator_performance = DataProcessor.process_translator_performance(all_records)
    system_performance = DataProcessor.process_system_performance_over_time(all_records)
    leaflet_performance = DataProcessor.process_leaflet_performance(all_records)

    # Generate insights
    translator_insights = AnalyticsGenerator.generate_translator_insights(translator_performance)
    system_insights = AnalyticsGenerator.generate_system_performance_insights(system_performance)
    leaflet_insights = AnalyticsGenerator.generate_leaflet_insights(leaflet_performance)

    # Print insights
    print("Translator Insights:")
    print("\n".join(translator_insights))
    print("\nSystem Performance Insights:")
    print("\n".join(system_insights))
    print("\nLeaflet Performance Insights:")
    print("\n".join(leaflet_insights))

    # Generate plots
    PlotGenerator.plot_translator_performance(translator_performance, 'bleu')
    PlotGenerator.plot_translator_performance(translator_performance, 'comet')
    PlotGenerator.plot_translator_performance(translator_performance, 'response_time')
    PlotGenerator.plot_system_performance_over_time(system_performance, 'bleu')
    PlotGenerator.plot_system_performance_over_time(system_performance, 'comet')
    PlotGenerator.plot_system_performance_over_time(system_performance, 'response_time')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'bleu')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'comet')
    PlotGenerator.plot_leaflet_performance(leaflet_performance, 'response_time')

if __name__ == "__main__":
    main()