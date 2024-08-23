# from typing import List, Dict
# from tqdm import tqdm
# from database.mongodb_client import MongoDBClient
# from data.entities import TranslationRecordEntity, TranslationEntity
# from utils.constants import EvaluationScoreType, BLEUScoreType
# from utils.logger import logger

# mongo_client = MongoDBClient.get_instance()


# def update_records():
#     all_records = get_all_records_from_db()

#     record_updated_count = 0
#     for record in tqdm(all_records, desc="Updating records"):
#         logger.info(f"========== Leaflet {record.evaluation_leaflet_data.leaflet_id}, Section {record.evaluation_leaflet_data.section_number}, Array Location {record.evaluation_leaflet_data.array_location} ==========")
#         try:
#             record = update_translation_record(record)
#             success, matched_count, modified_count = mongo_client.update_translation_record(record)
#             if success and matched_count > 0 and modified_count > 0:
#                 record_updated_count += 1
#             else:
#                 logger.error(f"Error updating record, matched_count: {matched_count}, modified_count: {modified_count}")
#         except Exception as e:
#             logger.error(f"========== Leaflet {record.evaluation_leaflet_data.leaflet_id}, Section {record.evaluation_leaflet_data.section_number}, Array Location {record.evaluation_leaflet_data.array_location} ==========")
#             logger.error(f"Error updating record, Error: {str(e)}")

#     logger.info(f"Updated {record_updated_count} records out of {len(all_records)} total records.")


# def get_all_records_from_db() -> List[TranslationRecordEntity]:
#     all_records = mongo_client.get_all_translation_records()
#     return all_records


# def update_translation_record(record: TranslationRecordEntity) -> TranslationRecordEntity:
#     record.translations = [delete_scores_from_translation(translation) for translation in record.translations]
#     record.best_translation = delete_scores_from_translation(record.best_translation)
    
#     return record
        

# # def update_translation_structure(translation: TranslationEntityOld) -> TranslationEntity:
# #     new_scores = update_scores_structure(translation.evaluation_scores)
    
# #     new_translation = TranslationEntity(
# #         translator_name     = translation.translator_name,
# #         translated_text     = translation.translated_text,
# #         response_time       = translation.response_time,
# #         score               = translation.score,
# #         evaluation_scores   = new_scores,
# #         metadata            = translation.metadata
# #     )

# #     return new_translation


# # def update_scores_structure(evaluation_scores: EvaluationScores) -> Dict[str, float]:
# #     bleu_scores = {
# #         BLEUScoreType.PLAIN_CORPUS.value:               evaluation_scores.bleu_plain_corpus,
# #         BLEUScoreType.TOKENIZED_CORPUS.value:           evaluation_scores.bleu_token_corpus,
# #         BLEUScoreType.TOKENIZED_METHOD1.value:          evaluation_scores.bleu_token_meth1,
# #         BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value:  evaluation_scores.bleu_token_meth1_w,
# #         # BLEUScoreType.TOKENIZED_METHOD7.value:          evaluation_scores.bleu_token_meth7,
# #         # BLEUScoreType.TOKENIZED_METHOD7_WEIGHTS.value:  evaluation_scores.bleu_token_meth7_w
# #     }

# #     new_scores = {
# #         EvaluationScoreType.BLEU.value:     bleu_scores,
# #         EvaluationScoreType.COMET.value:    evaluation_scores.comet_score,
# #         EvaluationScoreType.CHRF.value:     evaluation_scores.chrf_score,
# #         EvaluationScoreType.WER.value:      evaluation_scores.wer_score,
# #     }

# #     return new_scores

# def delete_scores_from_translation(translation: TranslationEntity) -> TranslationEntity:   
#     evaluation_scores = translation.evaluation_scores
#     bleu_scores = evaluation_scores[EvaluationScoreType.BLEU.value]

#     new_bleu_scores = {
#         BLEUScoreType.PLAIN_CORPUS.value:               bleu_scores[BLEUScoreType.PLAIN_CORPUS.value],
#         BLEUScoreType.TOKENIZED_CORPUS.value:           bleu_scores[BLEUScoreType.TOKENIZED_CORPUS.value],
#         BLEUScoreType.TOKENIZED_METHOD1.value:          bleu_scores[BLEUScoreType.TOKENIZED_METHOD1.value],
#         BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value:  bleu_scores[BLEUScoreType.TOKENIZED_METHOD1_WEIGHTS.value],
#         # BLEUScoreType.TOKENIZED_METHOD7.value:          evaluation_scores.bleu_token_meth7,
#         # BLEUScoreType.TOKENIZED_METHOD7_WEIGHTS.value:  evaluation_scores.bleu_token_meth7_w
#     }

#     new_scores = {
#         EvaluationScoreType.BLEU.value:     new_bleu_scores,
#         EvaluationScoreType.COMET.value:    evaluation_scores[EvaluationScoreType.COMET.value],
#         EvaluationScoreType.CHRF.value:     evaluation_scores[EvaluationScoreType.CHRF.value],
#         EvaluationScoreType.WER.value:      evaluation_scores[EvaluationScoreType.WER.value],
#     }

#     new_translation = TranslationEntity(
#         translator_name     = translation.translator_name,
#         translated_text     = translation.translated_text,
#         response_time       = translation.response_time,
#         score               = translation.score,
#         evaluation_scores   = new_scores,
#         metadata            = translation.metadata
#     )

#     return new_translation

# if __name__ == "__main__":
#     update_records()