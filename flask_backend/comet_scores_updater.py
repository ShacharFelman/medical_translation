from typing import List
from tqdm import tqdm
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, EvaluationScores
from services.evaluation.comet_evaluator import COMETEvaluator
from utils.logger import logger

def update_comet_scores():
    mongo_client = MongoDBClient.get_instance()
    comet_evaluator = COMETEvaluator()

    # Fetch all translation records from the database
    all_records = mongo_client.get_all_translation_records()
    
    updated_count = 0
    no_change_count = 0
    error_count = 0
    
    for record in tqdm(all_records, desc="Updating COMET scores"):
        if record.evaluation_leaflet_data and record.evaluation_leaflet_data.human_translation:
            record_updated = False
            for translation in record.translations:
                if translation.evaluation_scores and translation.evaluation_scores.comet_score is None:
                    try:
                        comet_score = comet_evaluator.evaluate(
                            reference_sentences=[record.evaluation_leaflet_data.human_translation],
                            hypothesis_sentences=[translation.translated_text],
                            source_sentences=[record.input]
                        )
                        translation.evaluation_scores.comet_score = comet_score
                        if (record.best_translation and 
                            record.best_translation.evaluation_scores and 
                            record.best_translation.evaluation_scores.comet_score is None and 
                            record.best_translation.translator_name == translation.translator_name):
                            record.best_translation.evaluation_scores.comet_score = comet_score
                        record_updated = True
                    except Exception as e:
                        logger.error(f"Error calculating COMET score for record: leaflet {record.evaluation_leaflet_data.leaflet_id} - section {record.evaluation_leaflet_data.section_number} - location {record.evaluation_leaflet_data.array_location} - translator {translation.translator_name}. Error: {str(e)}")
            
            if record_updated:
                try:
                    success, matched_count, modified_count = mongo_client.update_translation_record(record)
                    if success:
                        if modified_count > 0:
                            updated_count += 1
                        else:
                            no_change_count += 1
                            logger.info(f"No changes made to record: leaflet {record.evaluation_leaflet_data.leaflet_id} - section {record.evaluation_leaflet_data.section_number} - location {record.evaluation_leaflet_data.array_location}")
                    else:
                        error_count += 1
                        logger.warning(f"Failed to update record: leaflet {record.evaluation_leaflet_data.leaflet_id} - section {record.evaluation_leaflet_data.section_number} - location {record.evaluation_leaflet_data.array_location}")
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error updating record in database: leaflet {record.evaluation_leaflet_data.leaflet_id} - section {record.evaluation_leaflet_data.section_number} - location {record.evaluation_leaflet_data.array_location}. Error: {str(e)}")
    
    logger.info(f"Updated COMET scores for {updated_count} records out of {len(all_records)} total records.")
    logger.info(f"No changes were needed for {no_change_count} records.")
    logger.info(f"Encountered errors with {error_count} records.")

if __name__ == "__main__":
    update_comet_scores()