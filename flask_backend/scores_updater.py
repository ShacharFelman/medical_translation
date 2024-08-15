from typing import List
from tqdm import tqdm
from database.mongodb_client import MongoDBClient
from data.entities import TranslationRecordEntity, TranslationEntity, EvaluationScores
from services.evaluation.evaluation_manager import EvaluationManager


from utils.logger import logger

mongo_client = MongoDBClient.get_instance()
evaluation_manager = EvaluationManager()

# Set to True to override the existing scores
override_bleu = True
override_comet = False
override_chrf = False
override_wer = False

def update_scores():
    # Fetch all translation records from the database
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
                    translation_updated, new_evaluation_scores = update_translation_scores(translation, human_translation, input_text)
                    if translation_updated:
                        translation.evaluation_scores = new_evaluation_scores
                        record_updated = True
                        logger.info(f"Scores updated")

                    if (record.best_translation and 
                        record.best_translation.translator_name == translation.translator_name):
                        record.best_translation.evaluation_scores = new_evaluation_scores
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
                if is_translation_missing_score(translation):
                    # logger.info(f"Missing scores found for model {translation.translator_name}")
                    filtered_records.append(record)
                    break
    logger.info(f"Found {len(filtered_records)} records with missing scores")
    return filtered_records


def is_translation_missing_score(translation: TranslationEntity):
    if (not translation.evaluation_scores
        or translation.evaluation_scores is None
        or is_bleu_plain_corpus_missing(translation.evaluation_scores)
        or is_bleu_token_corpus_missing(translation.evaluation_scores)
        or is_bleu_token_meth1_missing(translation.evaluation_scores)
        or is_bleu_token_meth7_missing(translation.evaluation_scores)
        or is_bleu_token_meth1_w_missing(translation.evaluation_scores)
        or is_bleu_token_meth7_w_missing(translation.evaluation_scores)
        or is_comet_score_missing(translation.evaluation_scores)     
        or is_chrf_score_missing(translation.evaluation_scores)    
        # or is_wer_score_missing(translation.evaluation_scores)
        ):
        return True
    else:
        return False


def is_bleu_plain_corpus_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_plain_corpus or evaluation_scores.bleu_plain_corpus is None or override_bleu:
        return True
    else:
        return False

def is_bleu_token_corpus_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_token_corpus or evaluation_scores.bleu_token_corpus is None or override_bleu:
        return True
    else:
        return False
    
def is_bleu_token_meth1_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_token_meth1 or evaluation_scores.bleu_token_meth1 is None or override_bleu:
        return True
    else:
        return False
    
def is_bleu_token_meth7_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_token_meth7 or evaluation_scores.bleu_token_meth7 is None or override_bleu:
        return True
    else:
        return False
    
def is_bleu_token_meth1_w_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_token_meth1_w or evaluation_scores.bleu_token_meth1_w is None or override_bleu:
        return True
    else:
        return False
    
def is_bleu_token_meth7_w_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.bleu_token_meth7_w or evaluation_scores.bleu_token_meth7_w is None or override_bleu:
        return True
    else:
        return False

def is_comet_score_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.comet_score or evaluation_scores.comet_score is None or override_comet:
        return True
    else:
        return False


def is_chrf_score_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.chrf_score or evaluation_scores.chrf_score is None or override_chrf:
        return True
    else:
        return False
    

def is_wer_score_missing(evaluation_scores: EvaluationScores):
    if not evaluation_scores.wer_score or evaluation_scores.wer_score is None or override_wer:
        return True
    else:
        return False


def update_translation_scores(tranalsation: TranslationEntity, human_translation: str, input_text: str):
    scores_updated = False
    if tranalsation.evaluation_scores and tranalsation.evaluation_scores is not None:
        evaluation_scores = tranalsation.evaluation_scores
    else:
        evaluation_scores = EvaluationScores()

    # # Check if the bleu_plain_corpus score is missing and update it
    # if is_bleu_plain_corpus_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = evaluation_manager.update_translation_scores(tranalsation,
    #                                                                                    human_translation, "plain_corpus")
    #     if bleu_updated:
    #         scores_updated = True

    # # Check if the bleu_token_corpus score is missing and update it
    # if is_bleu_token_corpus_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = update_bleu_score(evaluation_scores, tranalsation.translated_text, human_translation, "token_corpus")
    #     if bleu_updated:
    #         scores_updated = True

    # # # Check if the bleu_token_meth1 score is missing and update it
    # if is_bleu_token_meth1_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = update_bleu_score(evaluation_scores, tranalsation.translated_text, human_translation, "token_meth1")
    #     if bleu_updated:
    #         scores_updated = True

    # # # Check if the bleu_token_meth7 score is missing and update it
    # if is_bleu_token_meth7_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = update_bleu_score(evaluation_scores, tranalsation.translated_text, human_translation, "token_meth7")
    #     if bleu_updated:
    #         scores_updated = True

    # # # Check if the bleu_token_meth1_w score is missing and update it
    # if is_bleu_token_meth1_w_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = update_bleu_score(evaluation_scores, tranalsation.translated_text, human_translation, "token_meth1_w")
    #     if bleu_updated:
    #         scores_updated = True

    # # # Check if the bleu_token_meth7_w score is missing and update it
    # if is_bleu_token_meth7_w_missing(evaluation_scores):
    #     bleu_updated, evaluation_scores = update_bleu_score(evaluation_scores, tranalsation.translated_text, human_translation, "token_meth7_w")
    #     if bleu_updated:
    #         scores_updated = True

    # # # Check if the COMET score is missing and update it
    # if is_comet_score_missing(evaluation_scores):
    #     comet_updated, evaluation_scores = update_comet_score(evaluation_scores, input_text, tranalsation.translated_text, human_translation)
    #     if comet_updated:
    #         scores_updated = True
    
    # # # Check if the chrF score is missing and update it
    # if is_chrf_score_missing(evaluation_scores):
    #     chrf_updated, evaluation_scores = update_chrf_score(evaluation_scores, tranalsation.translated_text, human_translation)
    #     if chrf_updated:
    #         scores_updated = True

    # # # Check if the WER score is missing and update it
    # if is_wer_score_missing(evaluation_scores):
    #     wer_updated, evaluation_scores = update_wer_score(evaluation_scores, tranalsation.translated_text, human_translation)
    #     if wer_updated:
    #         scores_updated = True


    return scores_updated, evaluation_scores


if __name__ == "__main__":
    update_scores()