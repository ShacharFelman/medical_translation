from data.entities import TranslationEntity
from data.boundaries import TranslationResponse, TranslatorLLMResponse

def translator_llm_response_to_entity(llm_response: TranslatorLLMResponse, response_time: float) -> TranslationEntity:
    return TranslationEntity(
        translator_name=llm_response.translator_name,
        translated_text=llm_response.translated_text,
        response_time=response_time,
        metadata=llm_response.metadata
    )

def entity_to_frontend_response(translation_entity: TranslationEntity) -> TranslationResponse:
    return TranslationResponse(
        translated_text=translation_entity.translated_text,
        translator_used=translation_entity.translator_name,
        confidence_score=translation_entity.score or 0.0
    )