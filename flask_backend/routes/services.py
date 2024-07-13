from flask import jsonify, request ,Blueprint
from utils.logger import logger
from utils.error_handlers import engine_not_initialized_response, missing_data_in_request_error, unsupported_source_language_error, unsupported_dest_language_error, internal_server_error
# from engine.engine import translation_engine
from utils.constants import Language
# from flask import send_file
# from datetime import datetime
# from io import BytesIO
# from docx import Document
# from docx.shared import Pt
# from docx.shared import RGBColor
# from htmldocx import HtmlToDocx
from engine.input_handling import input_validation_handler
from engine.output_handling import output_validation_handler
# from engine.cache import file_cache
# from engine.file_handling.file_text_extraction import get_word_document_text
# from engine.file_handling.files_processor import file_proccessor
from data.boundaries import TranslationRequest, TranslationResponse

from services.translation_manager import translation_manager

services_bp = Blueprint('services', __name__,url_prefix='')

def create_user_error(error_in_english:str,error_in_hebrew:str,status_code:int=500):
    return jsonify({"error":{
        "eng":error_in_english,
        "heb":error_in_hebrew
    }}),status_code


@services_bp.route('/text', methods=['POST'])
def translate_text():    
    if not translation_manager.is_initialized():
        return engine_not_initialized_response()   
    
    try:        
        data = request.json
        translation_request = TranslationRequest(
            source=data['source'],
            dest=data['dest'],
            text_input=data['textInput']
        )
    except Exception as e:
        logger.error(f"Error parsing request: {str(e)}")
        return missing_data_in_request_error()
    
    languages = [lang.value for lang in Language]
    if translation_request.source not in languages:
        return unsupported_source_language_error()
    if translation_request.dest not in languages:
        return unsupported_dest_language_error()

    try:
        translation_response: TranslationResponse = translation_manager.translate(translation_request)
        
        # Convert TranslationResponse to dictionary
        # response_data = {
        #     'translated_text': translation_response.translated_text,
        #     'translator_used': translation_response.translator_used,
        #     'confidence_score': translation_response.confidence_score
        # }
        
        return jsonify({'data': translation_response.translated_text}), 200
    except Exception as e:
        logger.error(f"Error during translation: {str(e)}")
        return internal_server_error()

######################################################################


# @services_bp.route('/html-docx', methods=['POST'])
# def download_docx(): 
#     try:        
#         data = request.json 
#         html_input = data['htmlInput']
#         new_parser = HtmlToDocx()
#         docx = new_parser.parse_html_string(html_input)
#         for paragraph in docx.paragraphs:
#             for run in paragraph.runs:
#                 run.font.name = "Arial" 
#                 run.font.size = Pt(11)      
#                 run.font.color.rgb = RGBColor(0, 0, 0)  
#         doc_buffer = BytesIO()
#         docx.save(doc_buffer)
#         doc_buffer.seek(0)      
#         return send_file(doc_buffer, as_attachment=True,download_name="generated_file.docx",mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  
        

