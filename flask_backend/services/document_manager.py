from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor
from htmldocx import HtmlToDocx
from utils.logger import logger
from utils.singleton_meta import SingletonMeta

class DocumentManager(metaclass=SingletonMeta):
    def __init__(self):
        self.html_to_docx = HtmlToDocx()

    def create_docx_from_html(self, html_content: str) -> BytesIO:
        try:
            # Replace newlines with HTML line breaks
            html_content = html_content.replace('\n', '<br>')

            # Create DOCX document from HTML
            docx = self.html_to_docx.parse_html_string(html_content)

            # Formatting the document
            self._format_document(docx)

            # Save the DOCX to a BytesIO object
            doc_buffer = BytesIO()
            docx.save(doc_buffer)
            doc_buffer.seek(0)

            return doc_buffer

        except Exception as e:
            logger.error(f"Error creating DOCX: {str(e)}")
            raise

    def _format_document(self, docx: Document):
        # Define font settings
        font_name = "Arial"
        font_color = RGBColor(0, 0, 0)

        # Update all styles in the document
        for style in docx.styles:
            if hasattr(style, 'font'):
                style.font.name = font_name
                style.font.color.rgb = font_color

        # Specific formatting for heading styles
        heading_sizes = {
            'Heading 1': 12,
            'Heading 2': 11,
            'Heading 3': 11,
            'Heading 4': 11
        }

        for style_name, size in heading_sizes.items():
            if style_name in docx.styles:
                style = docx.styles[style_name]
                style.font.size = Pt(size)
                style.font.bold = True
                if style_name == 'Heading 1':
                    style.font.underline = True

        # Ensure all paragraphs use the correct font
        for paragraph in docx.paragraphs:
            for run in paragraph.runs:
                run.font.name = font_name
                run.font.color.rgb = font_color
                if paragraph.style.name in heading_sizes:
                    run.font.size = Pt(heading_sizes[paragraph.style.name])
                    run.font.bold = True
                    if paragraph.style.name == 'Heading 1':
                        run.font.underline = True
                else:
                    run.font.size = Pt(11)

        # Set the default paragraph style
        docx.styles['Normal'].font.name = font_name
        docx.styles['Normal'].font.size = Pt(11)
        docx.styles['Normal'].font.color.rgb = font_color
    

document_manager = DocumentManager()