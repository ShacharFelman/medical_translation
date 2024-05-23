from singleton_meta import SingletonMeta

class FileProcessor(metaclass=SingletonMeta):
    def process(self,file_name:str,file_text:str) -> dict:
        return {
            "data":file_text,
            "raw_text": file_text,
            "filename":file_name,
        }

    
    

file_proccessor = FileProcessor()