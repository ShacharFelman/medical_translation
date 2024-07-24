import anthropic
from utils.exceptions import InvalidUserInputError
from utils.logger import logger
from .claude_llm_model import ClaudeLLMModel

class ClaudeTranslationModel(ClaudeLLMModel):
    '''
    Class for translating a paragraph using Claude 3. 

    Note that the class does not perform validation on the input (done by the prompt injection model) or the output (done by the claude validation model).
    '''
    translation_success_string = "[TRANSLATION SUCCESSFUL]"
    
    translation_failure_string = "[TRANSLATION FAILED]"

    system_prompt = f'''
As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.

The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise, well-structured, and coherent, capturing the essence of the original text. 

The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining the integrity of the original content.

Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.

Upon successful translation, please include the phrase {translation_success_string} at the end and only at the end of your response to indicate that the task has been completed effectively.

If the text you recieve contains no Hebrew text, contains no medical/pharmacological information or could not appear in a CMI leaflet, respond with {translation_failure_string}.

Provide a response without any additional information or comments besides the previously stated phrase and annotations.

Do not translate html tags and translate the texts inside each tag while keeping their output in their coresponding position.

For example, if I give you the following paragraph:

<heb_text>  אקמול היא תרופה לצינון. </heb_text>

Then your response will be:

<eng_text> Acamol is a medication for the common cold. </eng_text>

{translation_success_string}

'''
    def get_system_v4(self, full_leaflet_text):
        system_prompt = f'''

       As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.

The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise, well-structured, and coherent, capturing the essence of the original text. 

The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining the integrity of the original content.

Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.

Upon successful translation, please include the phrase {self.translation_success_string} at the end and only at the end of your response to indicate that the task has been completed effectively.

If the text you recieve contains no Hebrew text, contains no medical/pharmacological information or could not appear in a CMI leaflet, respond with {self.translation_failure_string}.

Provide a response without any additional information or comments besides the previously stated phrase and annotations.

Do not translate html tags and translate the texts inside each tag while keeping their output in their coresponding position.

For example, if I give you the following paragraph:

<heb_text>  אקמול היא תרופה לצינון. </heb_text>

Then your response will be:

<eng_text> Acamol is a medication for the common cold. </eng_text>

{self.translation_success_string}

use this text `{full_leaflet_text}` for comprehensive context and detailed understanding, ensuring accuracy in translation.

        '''
        return system_prompt
    
    

    def get_system_v3(self, full_leaflet_text):
        system_prompt = f'''

        As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.

        The translation should convey the original meaning, tone, and style, using precise, concise language that captures the essence of the original text. Ensure the translation reads naturally and fluently to English speakers, maintaining the integrity of the original content.

        Utilize bullet points and numbered lists where present in the original for clarity and structural integrity. Familiarize yourself with the full leaflet to capture its medical/pharmacological nuances and terminology accurately.

        Contain the translation within the tags: <eng_text> ... </eng_text>. Include the phrase {self.translation_success_string} at the end of your response to indicate a successful translation.

        If the received text contains no Hebrew, lacks medical information, or is inappropriate for a CMI leaflet, respond with {self.translation_failure_string}.

        **Translation Requirements:**
        1. **Accuracy and Clarity:** Maintain accuracy in medical terminology and clarity in instructions. Use concise language that is easy to understand.
        2. **Formatting Consistency:** Retain original formatting elements like bullet points and headings to preserve the document’s readability and structure.
        3. **Cultural and Idiomatic Precision:** Respect cultural nuances and idiomatic expressions to ensure the translation resonates with English-speaking audiences.
        4. **HTML Handling:** Preserve all HTML tags and attributes. Only translate the text within tags, maintaining their positions and functions.

        **Example Usage:**
        For example, if I give you the following paragraph:
        <heb_text> אקמול היא תרופה לצינון. </heb_text>

        Your response should be:
        <eng_text> Acamol is a medication for the common cold. </eng_text>
        {self.translation_success_string}

        **Reference Materials:**
        - **Full Leaflet Text for Reference:** Utilize `{full_leaflet_text}` for comprehensive context and detailed understanding, ensuring accuracy in translation.

        '''
        return system_prompt

    def get_system_v1(self,full_leaflet_text):
        system_prompt = f'''

    As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.

    The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise, well-structured, and coherent, capturing the essence of the original text. 

    The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining the integrity of the original content.

    Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.

    Before beginning the translation, review the full leaflet text to familiarize yourself with its terminology and style. This reference is crucial for ensuring that the translation captures the precise wording and medical/pharmacological nuances necessary for a CMI Leaflet.

    Upon successful translation, please include the phrase {self.translation_success_string} at the end and only at the end of your response to indicate that the task has been completed effectively.

    If the text you recieve contains no Hebrew text, contains no medical/pharmacological information or could not appear in a CMI leaflet, respond with {self.translation_failure_string}.

    Provide a response without any additional information or comments besides the previously stated phrase and annotations.

    Do not translate html tags and translate the texts inside each tag while keeping their output in their coresponding position.

    
    **Translation Requirements:**

    1. **Accuracy and Clarity:** The translation must convey the original message effectively, respecting the medical and cultural nuances of the source material. Familiarize yourself with the entire leaflet to capture its terminology and style accurately.
    2. **Fluency and Naturalness:** Ensure that the translated text reads as if originally written in English, retaining the integrity and essence of the Hebrew text.
    3. **Medical and Pharmacological Precision:** Utilize the provided English medical reference, and when available, the full Hebrew leaflet text for terminology and style guidance. This is crucial for the accuracy of disease descriptions, side effects, and patient instructions.
    4. Handling of HTML: Maintain all original HTML tags and attributes. Only the textual content within these tags should be translated. This approach ensures the structural integrity of the document is preserved.


    **Example Usage:**
    For example, if I give you the following paragraph:

    <heb_text>  אקמול היא תרופה לצינון. </heb_text>

    Then your response will be:

    <eng_text> Acamol is a medication for the common cold. </eng_text>
    {self.translation_success_string}


    **Reference Materials:**
    - **Full Leaflet Text for Reference:** Use `{full_leaflet_text}` for additional context and detailed understanding of the leaflet's content. This full text serves as a crucial reference to ensure contextual and terminological accuracy throughout the translation process.


    '''
        return system_prompt
    
    def get_system_v2(self,full_leaflet_text):
        system_prompt  = f"""
To incorporate the reference full text into the prompt, ensuring it is effectively utilized by the translator, here's how you can seamlessly integrate it into the revised prompt. This helps underline its importance as a resource for maintaining terminological consistency and accuracy:

---

**Translation Prompt for Hebrew to English Medical Leaflet**

**Objective:** As a model specializing in Hebrew to English translations, your task is to accurately translate a specific paragraph from a Consumer Medicine Information (CMI) leaflet, originally written in Hebrew. Ensure the translation is precise, maintains the original meaning, tone, style, and includes pertinent medical terminology, while being coherent and culturally nuanced.

**Source and Formatting:** Begin and end the translation within the tags `<heb_text>` and `</heb_text>`. The final translation should appear within `<eng_text>` and `</eng_text>`, maintaining the structural integrity of the original text.

**Translation Requirements:**

1. **Accuracy and Clarity:** The translation must convey the original message effectively, respecting the medical and cultural nuances of the source material. Familiarize yourself with the entire leaflet to capture its terminology and style accurately.
2. **Fluency and Naturalness:** Ensure that the translated text reads as if originally written in English, retaining the integrity and essence of the Hebrew text.
3. **Medical and Pharmacological Precision:** Utilize the provided English medical reference, and when available, the full Hebrew leaflet text for terminology and style guidance. This is crucial for the accuracy of disease descriptions, side effects, and patient instructions.
4. Handling of HTML: Maintain all original HTML tags and attributes. Only the textual content within these tags should be translated. This approach ensures the structural integrity of the document is preserved.

**Completion Indicators:**
- Include the phrase `{self.translation_success_string}` at the end of your response to indicate a successful translation.
- If the text does not contain relevant medical information, or if it deviates from what might appear in a CMI leaflet, indicate this with `{self.translation_failure_string}`.

**Annotations and Additional Information:**
- Do not translate HTML tags; however, ensure that the text inside each tag is accurately translated and kept in its corresponding position.
- Provide the translation without any extraneous comments or information, except for the phrases specified for indicating the success or failure of the translation.

**Example Usage:**
- If provided with the paragraph:
  `<heb_text>אקמול היא תרופה לצינון.</heb_text>`
- Your response should be:
  `<eng_text>Acamol is a medication for the common cold.</eng_text>`
  `{self.translation_success_string}`

**Reference Materials:**
- **Full Leaflet Text for Reference:** Use `{full_leaflet_text}` for additional context and detailed understanding of the leaflet's content. This full text serves as a crucial reference to ensure contextual and terminological accuracy throughout the translation process.

        """
        return system_prompt

    def translate_paragraph(self, paragraph_text: str,html_input,full_leaflet_text=None) -> str:

        if not self.is_valid_string_input(html_input):
            raise Exception("Translation Failed: Text cannot be empty")
        
        translation_message = f'<heb_text>\n{html_input}\n</heb_text>'
        system_prompt = self.get_system_v4(full_leaflet_text if full_leaflet_text else "")
        logger.error(system_prompt)
        response = self.send_claude_prompt(system_message = system_prompt, 
                                           text_prompt = translation_message, 
                                           stop_sequences = [self.translation_success_string])
        
        output_text = response.content[0].text

        return output_text
    
    def is_valid_response(self, response: anthropic.types.Message):   
        '''
        Checks if the response message from the API call is valid.
        '''   
        if not response.content:
            raise Exception("error: empty content from api response")

        if response.stop_reason == "max_tokens":
            raise InvalidUserInputError("text too long", "טקסט גדול מידי")

        if response.stop_reason ==  "stop_sequence":
            return True
        else:
            if self.translation_failure_string in response.content[0].text.upper():
                try:
                    logger.error(f"error in translation input: {response}")
                except:
                    pass
                raise InvalidUserInputError("Text is not medically related", "טקסט לא רפואי")
            try:
                logger.error(f"error in translation output: {response}")
            except:
                pass
            raise Exception(f"error in translation output: response did not stop on {self.translation_success_string}")

        # should not get here
        return False
    
    def remove_translation_tags(self, text: str) -> str:
        '''
        Removes the passed "translation tags" that were given in the prompt (<eng_text> and </eng_text>).

        Returns the string with the tags removed.

        '''
        text = text.strip()

        if text.startswith("<eng_text>") and text.endswith("</eng_text>"):    
            
            text = text.removeprefix("<eng_text>").removesuffix("</eng_text>")

            return text.strip()
        else:
            #should not technically get here without prompt injection
            raise Exception(f"error in translation output: {text}")