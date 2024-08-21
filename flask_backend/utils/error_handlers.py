from flask import jsonify
from utils.logger import logger


def handle_exception(error):
    logger.error(error)
    return internal_server_error()

def internal_server_error():
    return jsonify(
        {"error_message": 'internal server error'}
    ), 500

def invalid_user_input_error(error):
    return jsonify(
        {"error_message": error.english_message}
    ), 500

class InvalidUserInputError(Exception):
    def __init__(self, error_message:str) -> None:
        self.error_message = error_message
