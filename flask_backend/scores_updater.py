from typing import List
from tqdm import tqdm
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, TranslationEntity
from services.evaluation.evaluation_manager import EvaluationManager
from utils.constants import EvaluationScoreType, BLEUScoreType


from utils.logger import logger

mongo_client = MongoDBClient.get_instance()
evaluation_manager = EvaluationManager()

# Set to True to override the existing scores
overrides_scores = {
    EvaluationScoreType.BLEU.value:     False,
    EvaluationScoreType.COMET.value:    False,
    EvaluationScoreType.CHRF.value:     False,
    EvaluationScoreType.WER.value:      False
}

override_bleu_scores = {
    BLEUScoreType.PLAIN_CORPUS.value:               False,
    BLEUScoreType.TOKENIZED_CORPUS.value:           False,
    BLEUScoreType.TOKENIZED_METHOD1.value:          False,
    BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value:  False
}

def update_scores():
    all_records = get_all_records_from_db()
    filtered_records: List[TranslationRecordEntity] = filter_records_with_missing_scores(all_records)

    updated_count = 0
    no_change_count = 0
    error_count = 0
    
    for record in tqdm(filtered_records, desc="Updating scores"):
        if record.evaluation_leaflet_data and record.evaluation_leaflet_data.human_translation:
            logger.info(f"========== Leaflet {record.evaluation_leaflet_data.leaflet_id}, Section {record.evaluation_leaflet_data.section_number}, Array Location {record.evaluation_leaflet_data.array_location} ==========")
            record_updated = False
            input_text = record.input
            human_translation = record.evaluation_leaflet_data.human_translation
            for translation in record.translations:
                logger.info(f"========== {translation.translator_name}")
                if not translation.translated_text or translation.translated_text.strip() == "":
                    logger.warning(f"Skipping translation due to missing translated text")
                    continue
                try:
                    scores_updated, new_evaluation_scores = update_translation_scores(translation, human_translation, input_text)
                    if scores_updated:
                        translation.evaluation_scores = new_evaluation_scores
                        record_updated = True
                        logger.info(f"Scores updated")

                    if (record.best_translation and 
                        record.best_translation.translator_name == translation.translator_name):
                        record.best_translation.evaluation_scores = translation.evaluation_scores
                        logger.info(f"Best Translation scores updated after translation scores {'not ' if not record_updated else ''}updated")
                        record_updated = True

                except Exception as e:
                    logger.error(f"Error calculating score, Error: {str(e)}")
            
            if record_updated:
                try:
                    success, matched_count, modified_count = mongo_client.update_translation_record(record)
                    if success:
                        if modified_count > 0:
                            updated_count += 1
                        else:
                            no_change_count += 1
                            logger.info(f"No changes made")
                    else:
                        error_count += 1
                        logger.warning(f"Failed to update record")
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error updating record in database, Error: {str(e)}")
    
    logger.info(f"Updated scores for {updated_count} records out of {len(all_records)} total records.")
    logger.info(f"No changes were needed for {no_change_count} records.")
    logger.info(f"Encountered errors with {error_count} records.")


def get_all_records_from_db() -> List[TranslationRecordEntity]:
    all_records = mongo_client.get_all_translation_records()
    return all_records


def filter_records_with_missing_scores(records: List[TranslationRecordEntity]) -> List[TranslationRecordEntity]:
    filtered_records = []
    for record in records:
        if record.translations:
            for translation in record.translations:
                if is_translation_missing_any_score(translation):
                    filtered_records.append(record)
                    break
        if (record not in filtered_records and
            record.best_translation and
            is_translation_missing_any_score(record.best_translation)):
            filtered_records.append(record)
    logger.info(f"Found {len(filtered_records)} records with missing scores")
    return filtered_records


def is_translation_missing_any_score(translation: TranslationEntity):
    if is_evaluation_scores_missing(translation):
        return True   

    missing_scores = get_missing_score_types(translation)
    if (len(missing_scores) == 0):
        missing_bleu_scores = get_missing_bleu_types(translation)
        if len(missing_bleu_scores) == 0:
            return False
        
    return True
    

def is_evaluation_scores_missing(translation: TranslationEntity):
    return not translation.evaluation_scores or translation.evaluation_scores is None


def get_missing_score_types(translation: TranslationEntity):
    score_types = EvaluationScoreType.get_types()
    return [type for type in score_types if translation.evaluation_scores.get(type) is None or overrides_scores.get(type)]


def get_missing_bleu_types(translation: TranslationEntity):
    bleu_name = EvaluationScoreType.BLEU.value
    missing_bleu_scores = BLEUScoreType.get_types()
    if is_evaluation_scores_missing(translation):
        return missing_bleu_scores
    
    if bleu_name in get_missing_score_types(translation) or overrides_scores.get(bleu_name):
        return missing_bleu_scores

    bleu_scores = translation.evaluation_scores.get(bleu_name)
    missing_bleu_scores = [type for type in missing_bleu_scores if bleu_scores.get is None or override_bleu_scores.get(type)]
    return missing_bleu_scores


def update_translation_scores(tranalsation: TranslationEntity, human_translation: str, input_text: str):
    scores_updated = False
    missing_score_types = get_missing_score_types(tranalsation)
    missing_bleu_types = get_missing_bleu_types(tranalsation)
    if is_evaluation_scores_missing(tranalsation):
        evaluation_scores = None
        logger.info(f"evaluation_scores is missing")
    else:
        evaluation_scores = tranalsation.evaluation_scores
    logger.info(f"Missing scores: {missing_score_types}, {missing_bleu_types}")
    if len(missing_score_types) > 0:
        scores_updated, evaluation_scores = evaluation_manager.update_scores(evaluation_scores,
                                                                            human_translation,
                                                                            tranalsation.translated_text,
                                                                            input_text,
                                                                            missing_score_types,
                                                                            missing_bleu_types)
                        
    return scores_updated, evaluation_scores


if __name__ == "__main__":
    update_scores()