from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import RegexParser

# Translation Prompt Template
translation_success_string = "[TRANSLATION SUCCESSFUL]"
translation_failure_string = "[TRANSLATION FAILED]"

translation_prompt_template = f'''
As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.
The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise, well-structured, and coherent, capturing the essence of the original text.
The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining the integrity of the original content.
Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.
Upon successful translation, please include the phrase {translation_success_string} at the end and only at the end of your response to indicate that the task has been completed effectively.
If the text you receive contains no Hebrew text, contains no medical/pharmacological information or could not appear in a CMI leaflet, respond with {translation_failure_string}.
Provide a response without any additional information or comments besides the previously stated phrase and annotations.
Do not translate html tags and translate the texts inside each tag while keeping their output in their corresponding position.
For example, if I give you the following paragraph:
<heb_text> אקמול היא תרופה לצינון. </heb_text>
Then your response will be:
<eng_text> Acamol is a medication for the common cold. </eng_text> {translation_success_string}
'''

translation_prompt = ChatPromptTemplate.from_messages([("system", translation_prompt_template), ("user", "{text_input}")])

translation_parser = RegexParser(
    regex=r"<eng_text>([\s\S]*?)</eng_text>\s*(\[TRANSLATION (?:SUCCESSFUL|FAILED)\])",
    output_keys=["translated_text", "status"]
)