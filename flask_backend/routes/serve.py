from flask import send_from_directory,Blueprint
from logger import logger

static_bp = Blueprint('static', __name__,url_prefix='')

app_static_folder = "./react"

@static_bp.route('/static/css/<path:filename>')
def serve_css(filename):
    try:
        return send_from_directory("./react/static/css", filename)
    except Exception as e:
        logger.error(f"Error serving CSS file: {e}")

@static_bp.route('/static/js/<path:filename>')
def serve_js(filename):
    try:
        return send_from_directory("./react/static/js", filename)
    except Exception as e:
        logger.error(f"Error serving JavaScript file: {e}")

@static_bp.route('/')
def index():
    try:
        return send_from_directory(directory="./react", path='index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")    

