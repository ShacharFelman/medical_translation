
from services.evaluation.evaluators.bleu_evaluator import BLEUEvaluator
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction, corpus_bleu
from utils.logger import logger
from nltk.tokenize import word_tokenize
from utils.constants import BLEUScoreType


bleu_evaluator = BLEUEvaluator()

def calculate_blue_from_evaluator(human_translation, translated_text):
    
    for type in BLEUScoreType.get_types():
        logger.info(f"==================== EVALUATOR {type} ====================")
        bleu_score = bleu_evaluator.evaluate(
            human_translation,
            translated_text,
            type
        )
        logger.info(f"BLEU score: {bleu_score}")



# def calculate_bleu(human_translation, translated_text):
#     logger.info(f"==================== REGULAR ====================")
#     chencherry = SmoothingFunction()

#     human_translation, translated_text = human_translation.lower(), translated_text.lower()
#     human_translation, translated_text = format_text(human_translation, translated_text)

#     ref_length = len(human_translation[0])
#     cand_length = len(translated_text)
#     max_n = min(4, ref_length, cand_length)
#     weights = [1/max_n] * max_n + [0] * (4 - max_n)

#     score_sentence = sentence_bleu(human_translation, translated_text)
    
#     score_sentence_method1 = sentence_bleu(human_translation, translated_text, smoothing_function=SmoothingFunction().method1)
#     score_sentence_method7 = sentence_bleu(human_translation, translated_text, smoothing_function=SmoothingFunction().method7)
    
#     score_sentence_weights_method1 = sentence_bleu(human_translation, translated_text, weights=weights, smoothing_function=SmoothingFunction().method1)
#     score_sentence_weights_method7 = sentence_bleu(human_translation, translated_text, weights=weights, smoothing_function=SmoothingFunction().method7)

#     score_corpus = corpus_bleu(human_translation, translated_text)

#     logger.info(f"==========    sentence_blue   ==========")
#     logger.info(f"simple: {score_sentence}")
#     logger.info(f"method1: {score_sentence_method1}")
#     logger.info(f"method7: {score_sentence_method7}")
#     logger.info(f"method1, with weights: {score_sentence_weights_method1}")
#     logger.info(f"method7, with weights: {score_sentence_weights_method7}")
#     logger.info(f"===========   corpus_bleu     ==========")
#     logger.info(f"BLEU score, corpus: {score_corpus}")


# def calculate_bleu_tokenized(   human_translation, 
#                                 translated_text):
#     logger.info(f"==================== TOKENIZED ====================")
#     chencherry = SmoothingFunction()

#     human_translation, translated_text = human_translation.lower(), translated_text.lower()

#     tokenized_human_translations = [word_tokenize(human_translation)]
#     tokenized_translated_text = word_tokenize(translated_text)

#     ref_length = len(tokenized_human_translations[0])
#     cand_length = len(tokenized_translated_text)
#     max_n = min(4, ref_length, cand_length)
#     weights = [1/max_n] * max_n + [0] * (4 - max_n)

#     logger.info(f"tokenized_human_translations: {tokenized_human_translations}")
#     logger.info(f"tokenized_translated: {tokenized_translated_text}")

#     score_sentence = sentence_bleu(human_translation, translated_text)
    
#     score_sentence_method1 = sentence_bleu(tokenized_human_translations, tokenized_translated_text, smoothing_function=SmoothingFunction().method1)
#     score_sentence_method7 = sentence_bleu(tokenized_human_translations, tokenized_translated_text, smoothing_function=SmoothingFunction().method7)

#     score_sentence_weights_method1 = sentence_bleu(tokenized_human_translations, tokenized_translated_text, weights=weights, smoothing_function=SmoothingFunction().method1)
#     score_sentence_weights_method7 = sentence_bleu(tokenized_human_translations, tokenized_translated_text, weights=weights, smoothing_function=SmoothingFunction().method7)


#     score_corpus = corpus_bleu([tokenized_human_translations], [tokenized_translated_text])

#     logger.info(f"==========    sentence_blue   ==========")
#     logger.info(f"simple: {score_sentence}")
#     logger.info(f"method1: {score_sentence_method1}")
#     logger.info(f"method7: {score_sentence_method7}")
#     logger.info(f"method1, with weights: {score_sentence_weights_method1}")
#     logger.info(f"method7, with weights: {score_sentence_weights_method7}")
#     logger.info(f"===========   corpus_bleu     ==========")
#     logger.info(f"BLEU score, corpus: {score_corpus}")


# def format_text(human_translation: str, translated_text: str):
#     human_translation = [[human_translation]] if isinstance(human_translation, str) else human_translation
#     translated_text = [translated_text] if isinstance(translated_text, str) else translated_text
#     return human_translation, translated_text

if __name__ == "__main__":
    
    human_translate1 = "If a side effect occurs, if one of the side effects worsens, or if you suffer from a side effect not mentioned in this leaflet, consult your kdfjhgsdkfgh."
    translated_text1 = "If a side effect occurs, if one of the side effects worsens, or if you suffer from a side effect not mentioned in this leaflet, consult your doctor."

    human_translate2 = "Fever"
    translated_text2 = "Fever"

    human_translate3 = "Side effects of unknown frequency which are not listed in this leaflet"
    translated_text3 = "Side effects the unknown frequency which are not listed in this leaflet"

    human_translate4 = "Drug Interaction"
    translated_text4 = "Drug interactions"

    human_translate8 = "Interactions"
    translated_text8 = "interactions"

    human_translate5 = "Severe skin reactions"
    translated_text5 = "Serious skin reactions"

    human_translate6 = "as such supplements,"
    translated_text6 = "At the appropriate dosage,"
    
    human_translate7 = "                TO STORE THE MEDICINE"
    translated_text7 = "TO store the     ?        MEDICINE"
    
    human_translate9 = "TO STORE THE MEDICINE"
    translated_text9 = "TO store the medication"
    
    
    human_translate10 = "Important information about some of the ingredients of the medicine"
    translated_text10 = "Important information about some of the ingredients in the medicine"
  
    human_translation, translated_text = (human_translate7,
                                          translated_text7
                                          )

    # calculate_blue_from_evaluator(human_translation, translated_text)

    # calculate_bleu(human_translation, translated_text)

    calculate_blue_from_evaluator(human_translation, translated_text)



    