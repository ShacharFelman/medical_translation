from flask import jsonify,Blueprint

api_bp = Blueprint('api', __name__,url_prefix='/api')

@api_bp.route('/ping', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def ping():
    return jsonify({'message': {
        "eng":'server is running',
        "heb":"סרבר רץ"}}), 200


@api_bp.route('/error', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def error_ping():
    return jsonify({'error': {
        "eng":'some error',
        "heb":"שגיאה בדיקה"

        }}), 500
