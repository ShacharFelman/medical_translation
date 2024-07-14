from data.entities import TranslationEntity, LeafletHistoryEntity, LeafletSectionEntity
from data.boundaries import TranslationResponse, TranslatorLLMResponse, LeafletSaveRequest, LeafletSectionInput


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

def leaflet_save_request_to_entity(save_request: LeafletSaveRequest) -> LeafletHistoryEntity:
    sections = [
        LeafletSectionEntity(
            id=section.id,
            input_text=section.input_text,
            translated_text=section.translated_text
        ) for section in save_request.sections
    ]
    return LeafletHistoryEntity(
        name=save_request.name,
        date=save_request.date,
        sections=sections
    )

def leaflet_history_entity_to_save_request(entity: LeafletHistoryEntity) -> LeafletSaveRequest:
    sections = [
        LeafletSectionInput(
            id=section.id,
            input_text=section.input_text,
            translated_text=section.translated_text
        ) for section in entity.sections
    ]
    return LeafletSaveRequest(
        name=entity.name,
        date=entity.date,
        sections=sections
    )