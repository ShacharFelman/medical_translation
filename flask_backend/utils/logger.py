import logging
import os

level = os.environ.get('LOG_LEVEL',logging.INFO)

logs_dir = os.environ.get('LOGS_DIR',None)

handlers = [logging.StreamHandler()]

if logs_dir:
    os.makedirs(logs_dir,exist_ok=True)

    handlers = [
        logging.FileHandler(f"{logs_dir}/last_run.log",mode='w'),
        logging.FileHandler(f"{logs_dir}/all.log",mode='a'),
        logging.StreamHandler()
    ]

logging.basicConfig(level=level, 
                    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
                    handlers=handlers)                    

logger = logging.getLogger(__name__)