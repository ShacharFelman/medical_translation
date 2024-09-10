from langchain_core.prompts import ChatPromptTemplate
import re

# Translation Prompt Template
translation_success_string = "[TRANSLATION SUCCESSFUL]"

translation_prompt_template = f'''
As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph
from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.
The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the
leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise,
well-structured, and coherent, capturing the essence of the original text.
The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining
the integrity of the original content. Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.
Upon successful translation, please include the phrase {translation_success_string} at the end and only at the end of your response
to indicate that the task has been completed effectively.
The input text may contain HTML tags, which should be preserved in their original form. Translate only the content within the tags,
keeping the tags themselves unchanged and in their original positions.
Do not translate HTML tags and translate the texts inside each tag while keeping their output in their corresponding position.
For example, if I give you the following paragraph:
<heb_text> אקמול היא <b>תרופה</b> לצינון. </heb_text>
Then your response will be:
<eng_text> Acamol is a <b>medicine</b> for the common cold. </eng_text> {translation_success_string}
Provide a response without any additional information or comments besides the previously stated phrase and annotations.
'''

translation_prompt = ChatPromptTemplate.from_messages([("system", translation_prompt_template), ("user", "<heb_text>{text_input}</heb_text>")])

class TranslationParser:
    def parse(self, text) -> str:
        if text is None:
            return ""
        
        # Strip leading and trailing whitespace from the input text
        text = text.strip()
        
        # Remove the final "[TRANSLATION SUCCESSFUL]" string
        text = re.sub(r'\[TRANSLATION SUCCESSFUL\]\s*$', '', text)
        
        # Remove the "<eng_text>" and "</eng_text>" tags if they exist
        text = re.sub(r'</?eng_text>', '', text)
        
        # Strip any remaining whitespace after all manipulations
        text = text.strip()
        
        return {
            "translated_text": text,
            "status": "[TRANSLATION SUCCESSFUL]"
        }
    
    def remove_html_tags(self, text) -> str:
        if text is None:
            return ""

        # Define replacements for whitespace-related entities
        whitespace_entities = {
            '&nbsp;': ' ',
            '&ensp;': ' ',
            '&emsp;': '    ',
            '&thinsp;': ' ',
            '&tab;': '\t',
            '&#9;': '\t',  # Tab character
            '&#10;': '\n',  # Line feed
            '&#13;': '\r',  # Carriage return
        }

        # Replace whitespace-related entities
        for entity, replacement in whitespace_entities.items():
            text = text.replace(entity, replacement)
            text = text.replace(entity.upper(), replacement)  # Handle uppercase variants

        # Function to add newline after block-level elements
        def add_newline_after_tag(match):
            return match.group(1) + '\n'

        # List of block-level HTML elements that should have a newline after them
        block_tags = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'th', 'td', 
                      'section', 'article', 'header', 'footer', 'nav', 'aside', 'blockquote', 
                      'address', 'pre', 'figure', 'figcaption', 'ol', 'ul', 'dl', 'dt', 'dd']

        # Process block-level elements
        for tag in block_tags:
            text = re.sub(f'<{tag}[^>]*>(.*?)</{tag}>', add_newline_after_tag, text, flags=re.DOTALL | re.IGNORECASE)

        # Handle self-closing tags that create line breaks
        text = re.sub(r'<(br|hr)[^>]*/?>', '\n', text, flags=re.IGNORECASE)

        # Remove all remaining HTML tags
        text = re.sub('<[^<]+?>', '', text)

        # Replace multiple spaces with a single space
        text = re.sub(r' +', ' ', text)

        # Replace multiple newlines with a maximum of two newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text

translation_parser = TranslationParser()