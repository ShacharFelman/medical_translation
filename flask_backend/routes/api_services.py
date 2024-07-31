from flask import jsonify, request ,Blueprint
from typing import Optional
from utils.logger import logger
from utils.constants import Language
from utils.exceptions import InvalidUserInputError
from flask import send_file
from io import BytesIO
from docx.shared import Pt
from docx.shared import RGBColor
from htmldocx import HtmlToDocx
from pydantic import ValidationError
from data.boundaries import TranslationRequest, TranslationResponse, LeafletSaveRequest, LeafletResponse, FetchLeafletsResponse, TranslationDownloadRequest
from services.translation_manager import TranslationManager
from services.history_manager import history_manager
from services.translation.runtime_translation_handler import RuntimeTranslationHandler


api_services_bp = Blueprint('api_services', __name__,url_prefix='')

def create_error_response(error_message:str='Internal Server Error', status_code:int=500):
    return jsonify(
        {"error_message":error_message}
    ),status_code


@api_services_bp.route('/translate', methods=['POST'])
def translate_text():    
    translation_manager = TranslationManager(RuntimeTranslationHandler())
    translation_manager.initialize()

    if not translation_manager.is_initialized():
        return create_error_response("Translation engine is still loading. Please wait...", 503)
    
    try:        
        data = request.json
        translation_request = TranslationRequest(**data)
    except Exception as e:
        logger.error(f"Error parsing request: {str(e)}")
        return create_error_response("Invalid data in request", 400)
    
    languages = [lang.value for lang in Language]
    if translation_request.source not in languages:
        return create_error_response("Source language is not supported", 400)
    if translation_request.dest not in languages:
        return create_error_response("Destination language is not supported", 400)

    try:
        translation_response: TranslationResponse = translation_manager.translate(translation_request)
        
        if not translation_response.translated_text:
            logger.error("Translation failed: Empty translated text")
            return create_error_response("Translation failed", 500)
        
        return jsonify({'data': translation_response.translated_text}), 200
    except InvalidUserInputError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error during translation: {str(e)}")
        return create_error_response("Internal server error", 500)
    

@api_services_bp.route('/save-leaflet', methods=['POST'])
def save_leaflet():     
    try:        
        data = request.json
        save_request = LeafletSaveRequest(**data)
        result: Optional[LeafletResponse] = history_manager.save_leaflet(save_request)
        
        if result:
            return jsonify(result.model_dump()), 200
        else:
            return create_error_response("Failed to save leaflet", 500)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_error_response("Invalid data", 400)

    except Exception as e:
        logger.error(f"Error saving leaflet: {str(e)}")
        return create_error_response("Internal server error", 500)
    
    
@api_services_bp.route('/fetch-leaflets', methods=['GET'])
def fetch_leaflets():
    try:
        result: FetchLeafletsResponse = history_manager.fetch_all_leaflets()
        
        if not result.leaflets:
            return create_error_response("No leaflets found", 404)

        return jsonify(result.model_dump()), 200

    except Exception as e:
        logger.error(f"Error fetching leaflets: {str(e)}")
        return create_error_response("Internal server error", 500)
    

@api_services_bp.route('/delete-leaflet/<leaflet_id>', methods=['DELETE'])
def delete_leaflet(leaflet_id):
    try:
        result = history_manager.delete_leaflet(leaflet_id)
        
        if result:
            return jsonify({"message": "Leaflet deleted"}), 200
        else:
            return create_error_response("Failed to delete leaflet", 500)

    except Exception as e:
        logger.error(f"Error deleting leaflet: {str(e)}")
        return create_error_response("Internal server error", 500)


@api_services_bp.route('/download-docx', methods=['POST'])
def download_docx(): 
    try:        
        data = request.json 
        downloadRequest = TranslationDownloadRequest(
            input=data['input'].replace('\n', '<br>'))

        # Create DOCX document from HTML
        new_parser = HtmlToDocx()
        docx = new_parser.parse_html_string(downloadRequest.input)

        # Formatting the document
        for paragraph in docx.paragraphs:
            for run in paragraph.runs:
                run.font.name = "Arial" 
                run.font.size = Pt(11)      
                run.font.color.rgb = RGBColor(0, 0, 0)

        # Save the DOCX to a BytesIO object
        doc_buffer = BytesIO()
        docx.save(doc_buffer)
        doc_buffer.seek(0)    
  
        return send_file(doc_buffer, as_attachment=True,download_name="generated_file.docx",mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        logger.error(f"Error creating DOCX: {str(e)}")
        return create_error_response("Internal server error", 500)

