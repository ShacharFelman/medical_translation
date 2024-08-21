import os
from flask import Flask
from flask_cors import CORS
from flask.logging import default_handler
from utils.error_handlers import handle_exception, invalid_user_input_error, InvalidUserInputError
from routes import api_services_bp

def create_app():
    app = Flask(__name__,static_folder="</>",static_url_path='')
    
    app.logger.removeHandler(default_handler)    

    SECRET_KEY = os.environ.get('SECRET_KEY',None)
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    app.config['SECRET_KEY'] = SECRET_KEY

    FLASK_ENV = os.environ.get('FLASK_ENV',None)
    if not FLASK_ENV:
        raise ValueError("No FLASK_ENV set for Flask application")
    
    app.register_error_handler(InvalidUserInputError, invalid_user_input_error)
    app.register_error_handler(Exception, handle_exception) 

    app.register_blueprint(api_services_bp)
    if FLASK_ENV == "development" or FLASK_ENV == "testing":
        CORS(app) 
    else:
        pass

    with app.app_context():
        pass
    
    return app


app = create_app()


def main():
    FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST',"0.0.0.0")
    PORT = os.environ.get('PORT',5000)
    if not FLASK_RUN_HOST:
        raise ValueError("No FLASK_RUN_HOST set for Flask application")
    if not PORT:
        raise ValueError("No PORT set for Flask application")
    app.run(host=FLASK_RUN_HOST,port=PORT)    

        
if __name__ == "__main__": # This only run in development
    main()