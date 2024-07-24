from .claude_llm_model import ClaudeLLMModel
from utils.logger import logger
class ClaudeValidationModel(ClaudeLLMModel):
    
    translation_valid_string = '[TRANSLATION VALID]'

    translation_invalid_string = '[TRANSLATION INVALID]'

    system_prompt = f'''
Validate the given text within the tags <eng_text> ... </eng_text> to confirm if it is in English, if it would appear in a CMI Leaflet and if it contains medical/pharmacological terminology. Please ignore any HTML tags that may appear within the text.

Before beginning the validation, review the full leaflet text to familiarize yourself with its terminology and style. This reference is crucial for ensuring that the translation captures the precise wording and medical/pharmacological nuances necessary for a CMI Leaflet.

If the text within the annotation meets these criteria, reply only with the following text: {translation_valid_string}. 

Otherwise, respond with {translation_invalid_string}.

Your response should be clear, concise, and free of any additional information or comments.

Here are a few examples:

Example 1:
<eng_text> Acamol is a medication for the common cold. </eng_text>
Your reply: {translation_valid_string}

Example 2:
<eng_text> Take <b>two tablets</b> with water. </eng_text>
Your reply: {translation_valid_string}

Example 3:
<eng_text> The first ten elements of the Fibonacci sequence are: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34. </eng_text>
Your reply: {translation_valid_string}

Example 4:
<eng_text> Ce médicament est utilisé pour traiter la douleur. </eng_text>
Your reply: {translation_invalid_string}

Example 5:
<eng_text> Ce médicament <b>est utilisé</b> pour traiter la douleur. </eng_text>
Your reply: {translation_invalid_string}

Example 6:
<eng_text> My name is <b>claude</b> </eng_text>
Your reply: {translation_invalid_string}

'''
    
    def get_system_prompt(self,full_leaflet_text):
        system_prompt = f'''
    Validate the given text within the tags <eng_text> ... </eng_text> to confirm if it is in English, if it would appear in a CMI Leaflet and if it contains medical/pharmacological terminology. Please ignore any HTML tags that may appear within the text.

    Before beginning the validation, review the full leaflet text to familiarize yourself with its terminology and style. This reference is crucial for ensuring that the translation captures the precise wording and medical/pharmacological nuances necessary for a CMI Leaflet.

    If the text within the annotation meets these criteria, reply only with the following text: {self.translation_valid_string}. 

    Otherwise, respond with {self.translation_invalid_string}.

    Your response should be clear, concise, and free of any additional information or comments.

    Here are a few examples:

    Example 1:
    <eng_text> Acamol is a medication for the common cold. </eng_text>
    Your reply: {self.translation_valid_string}

    Example 2:
    <eng_text> Take <b>two tablets</b> with water. </eng_text>
    Your reply: {self.translation_valid_string}

    Example 3:
    <eng_text> The first ten elements of the Fibonacci sequence are: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34. </eng_text>
    Your reply: {self.translation_valid_string}

    Example 4:
    <eng_text> Ce médicament est utilisé pour traiter la douleur. </eng_text>
    Your reply: {self.translation_invalid_string}

    Example 5:
    <eng_text> Ce médicament <b>est utilisé</b> pour traiter la douleur. </eng_text>
    Your reply: {self.translation_invalid_string}

    Example 6:
    <eng_text> My name is <b>claude</b> </eng_text>
    Your reply: {self.translation_invalid_string}

    the full leaflet text for reference during validation:
        {full_leaflet_text} 

    '''
        return system_prompt
        

    def validate_translation(self, translation_text: str) -> bool:
        '''
        Returns true if translation is in English, could appear in a CMI Leaflet and contains medical/pharmacological information.
        '''
        
        response = self.send_claude_prompt(system_message = self.system_prompt, 
                                           text_prompt = translation_text, 
                                           stop_sequences = [self.translation_valid_string])

        # since [TRANSLATION_VALID] is the stop sequence, it will not be included in claude's response, meaning the response would be empty. If there is content in the response, the translation fails.
        
        if not response.content:
            return True
        
        return False