from flask import jsonify
from logger import logger


def handle_invalid_user_input_error(error):
    return jsonify({
        'error': {
            "eng": str(error.english_message),
            "heb": str(error.hebrew_message)
        }
    }), 400

def handle_exception(error):
    logger.error(error)
    return jsonify({
        'error': {
            "eng": 'internal server error',
            "heb": "בעיה בסרבר"
        }
    }), 500