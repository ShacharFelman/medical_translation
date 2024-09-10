from database.mongodb_client import MongoDBClient

def get_translation_insights():
    # Connect to MongoDB
    mongo_client = MongoDBClient.get_instance()

    # Get all translation records
    records = mongo_client.get_all_translation_records()

    # 1. Total number of records
    total_records = len(records)

    # 2. Total input words
    total_input_words = sum(len(record.input.split()) for record in records)

    # 3. Total output words (best translations)
    total_output_words = sum(len(record.best_translation.translated_text.split()) for record in records if record.best_translation)

    # 4. Total output tokens (best translations)
    total_output_tokens = sum(
        record.best_translation.metadata.get('usage', {}).get('output_tokens', 0)
        for record in records
        if record.best_translation and 'usage' in record.best_translation.metadata
    )

    return {
        "total_records": total_records,
        "total_input_words": total_input_words,
        "total_output_words": total_output_words,
        "total_output_tokens": total_output_tokens
    }

if __name__ == "__main__":
    insights = get_translation_insights()
    print("Translation Insights:")
    print(f"1. Total records: {insights['total_records']}")
    print(f"2. Total input words: {insights['total_input_words']}")
    print(f"3. Total output words: {insights['total_output_words']}")
    print(f"4. Total output tokens: {insights['total_output_tokens']}")