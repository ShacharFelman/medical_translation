from flask import jsonify
from utils.logger import logger


def handle_exception(error):
    logger.error(error)
    return internal_server_error()

def invalid_user_input_error(error):
    return jsonify({
        'error': {
            "eng": str(error.english_message),
            "heb": str(error.hebrew_message)
        }
    }), 400

def internal_server_error():
    return jsonify({
        'error': {
            "eng": 'internal server error',
            "heb": "בעיה בשרת"
        }
    }), 500

def missing_data_in_request_error():
    return jsonify({'error': {
        "eng":"missing data in request",
        "heb":"בעיה בעיבוד הבקשה, חסרים נתונים"
        }}), 400

def unsupported_source_language_error():
        return jsonify({'error': {
            "eng": "source language is not supported",
            "heb": "שפת התרגום לא קיימת"
        }}), 400

def unsupported_dest_language_error():
        return jsonify({'error': {
            "eng": "dest language is not supported",
            "heb": "שפה המוצא לא קיימת"
        }}), 400
    
def engine_not_initialized_response():
    return jsonify({'error': {
        "eng": 'translation engine is still loading. Please wait...',
        "heb": "מודל התרגום בטעינה, אנא המתן..."
    }}), 503