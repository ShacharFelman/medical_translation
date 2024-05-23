from flask import jsonify, request ,Blueprint
from logger import logger
from exceptions import InvalidUserInputError
from engine.engine import translation_engine
from constants import Language
from flask import send_file
from datetime import datetime
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor
from htmldocx import HtmlToDocx
from engine.input_handling import input_validation_handler
from engine.output_handling import output_validation_handler
from engine.cache import file_cache
from engine.file_handling.file_text_extraction import get_word_document_text
from engine.file_handling.files_processor import file_proccessor
services_bp = Blueprint('services', __name__,url_prefix='')

def create_user_error(error_in_english:str,error_in_hebrew:str,status_code:int=500):
    return jsonify({"error":{
        "eng":error_in_english,
        "heb":error_in_hebrew
    }}),status_code

def create_interval_error():
    return jsonify({"error":{
        "eng":"interval server error",
        "heb":"בעיה בסרבר"
    }}),500



@services_bp.route('/reference', methods=['POST'])
def upload_reference_file():    
    file = request.files.get('file')
    if not file:
        return jsonify({'error': {
            "eng":"file not found",
            "heb":"קובץ לא נמצא"
            }}), 404    
    
    if file.filename == '':
        return jsonify({'error': {
            "eng":'no selected file',
            "heb":"קובץ לא נבחר"
        }}), 400    
    
    if not file.filename.endswith(".docx") and not file.filename.endswith(".doc"):
        raise InvalidUserInputError("file type is  not supported, please upload a word document","קובץ אינו נתמך אנא השתמש בקובץ וורד")


    file_text = get_word_document_text(file)

    # upload reference file after proccesing
    file_data = file_proccessor.process(file.filename,file_text)
    reference_token = file_cache.register_file(file.filename,file_text,file_data)
    # return cache token 
    return jsonify({'data':{"reference_token": reference_token}}), 200


@services_bp.route('/text', methods=['POST'])
def translate_text():    
    if not translation_engine.is_initialized():
        return jsonify({'error': {
            "eng":'translation engine is still loading. Please wait...',
            "heb":"נא להתמין למודל לעלות..."
            }}), 503    
    
    try:        
        data = request.json
        reference_token = data['referenceToken']
        source = data['source']
        dest = data['dest']
        text_input = data['textInput']    
        html_input = data['htmlInput']
    except Exception as e:
        logger.error(e)
        return jsonify({'error': {
            "eng":"missing data in request",
            "heb":"מידע חסר בבקשה"
            }}), 400
    languages = [lang.value for lang in Language]
    if source not in languages:
        return jsonify({'error': {
            "eng":"source language is not supported",
            "heb":"שפת התרגום לא קיימת"}}), 400
    if dest not in languages:
        return jsonify({'error': {
            "eng":"dest language is not supported",
            "heb":"שפה המוצא לא קיימת"
            }}), 400

    errors = input_validation_handler.get_errors(text_input)
    if len(errors) > 0:
        for error in errors:
            logger.error(error)
        return jsonify({'error': "invalid input"}), 422
    
    processed_data = file_cache.get(reference_token)
    output_text = translation_engine.translate(processed_data,dest,source,text_input,html_input)

    errors = output_validation_handler.get_errors(output_text)
    if len(errors) > 0:
        for error in errors:
            logger.error(error)
        return create_interval_error()

    return jsonify({'data': output_text}), 200



@services_bp.route('/html-docx', methods=['POST'])
def download_docx(): 
    try:        
        data = request.json 
        html_input = data['htmlInput']
        new_parser = HtmlToDocx()
        docx = new_parser.parse_html_string(html_input)
        for paragraph in docx.paragraphs:
            for run in paragraph.runs:
                run.font.name = "Arial" 
                run.font.size = Pt(11)      
                run.font.color.rgb = RGBColor(0, 0, 0)  
        doc_buffer = BytesIO()
        docx.save(doc_buffer)
        doc_buffer.seek(0)      
        return send_file(doc_buffer, as_attachment=True,download_name="generated_file.docx",mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
        

