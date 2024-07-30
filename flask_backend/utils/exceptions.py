import traceback
from utils.logger import logger

class UnsupportedLanguageError(Exception):
    def __init__(self, message:str) -> None:
        logger.error(f'Unsupported Language {message}')
        super().__init__(message)


class UnsupportedInputFileTypeError(Exception):
    def __init__(self, message:str) -> None:
        logger.error(f'Unsupported Input File Type {message}')
        super().__init__(message)



class InsertionException(Exception):
    def __init__(self, message:str) -> None:
        logger.error(f'Insertion Exception: {message}')
        super().__init__(message)
    


class ExtractionException(Exception):
    def __init__(self, message:str) -> None:
        logger.error(f'Extraction Exception: {message}')
        super().__init__(message)

class ExtractionFormatError(ExtractionException):
    def __init__(self, message:str) -> None:
        super().__init__(f'Format Error: {message}')
    

class UnsupportedOutputFileTypeError(InsertionException):
    def __init__(self, message:str) -> None:
        super().__init__(f'UnSupported Output File Type: {message}')
    

class InvalidUserInputError(Exception):
    def __init__(self, error_message:str) -> None:
        self.error_message = error_message
