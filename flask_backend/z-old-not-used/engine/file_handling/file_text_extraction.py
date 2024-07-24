from io import BytesIO
from docx import Document
from utils.constants import FileType

def get_word_document_text(file):
    file_type = FileType.get_file_type(file.filename)
    if not file_type:
        return
    if file_type == FileType.DOCX or file_type == FileType.DOC:
        file_content = file.read()
        docx_document = Document(BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in docx_document.paragraphs])
        return text