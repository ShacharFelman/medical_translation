# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# from typing import List
# from engine.model.gpt.base_gpt_translation_model import BaseGPTTranslationModel
# from openai_function_tokens import estimate_tokens
# from logger import logger
# import functools

# from exceptions import InvalidUserInputError


# class GPT4TranslationModel(BaseLLMTranslationModel):
#     model_name = 'gpt-4-0125-preview'
#     token_max_limit = 4096

#     translation_success_string = "[translation successful]"
#     # prompt #1: 
#     # system_prompt =  f'''I'm looking for assistance in translating a specific paragraph from a CMI leaflet, originally in Hebrew, into English. The goal is to achieve a translation that not only accurately reflects the original meaning but also retains the original tone, style, and any pertinent terminology. It's crucial that the translation feels natural and fluent to English speakers, effectively conveying the leaflet's message while respecting cultural nuances and idiomatic expressions unique to the source material. The final translation should be precise, well-structured, and coherent, truly capturing the essence of the original text. Upon successful translation, please include the phrase '{translation_success_string}' at the end of your response to indicate the task has been completed effectively.'''
#     # prompt #2: 
#     # system_prompt = f'''Please translate the following paragraph from a CMI leaflet from Hebrew to English. Your translation should accurately convey the meaning of the original paragraph in clear and fluent English, maintaining the same tone and style as the source text. Pay attention to preserving any specific terminology or context that is relevant to the content of the leaflet. Your translation should be precise and well-structured, ensuring that the message is effectively communicated to an English-speaking audience. Please aim for a natural and coherent translation that captures the essence of the original paragraph while considering cultural nuances and idiomatic expressions. Upon successful translation, please include the phrase '{translation_success_string}' at the end of your response to indicate the task has been completed effectively.'''
#     # prompt #3:
#     system_prompt = f'''Please translate a specific paragraph from a CMI leaflet, originally in Hebrew, into English. The translation should accurately reflect the original meaning, retain the original tone, style, and any pertinent terminology, and effectively convey the leaflet's message while respecting cultural nuances and idiomatic expressions unique to the source material. The final translation should be precise, well-structured, and coherent, truly capturing the essence of the original text. Upon successful translation, please include the phrase {translation_success_string} at the end of your response to indicate the task has been completed effectively. Your translation should feel natural and fluent to English speakers, ensuring that it reads like an original English text while maintaining the integrity of the original content.'''
#     system_prompt_message = [{"role": "system", "content": system_prompt}]

#     def __init__(self):
#         load_dotenv()
#         self.api_key = os.getenv('OPENAI_API_KEY')
#         self.client = OpenAI(api_key=self.api_key)

#     def translate_document(self, document_text: List[str]) -> List[str]:
#         messages = self.system_prompt_message.copy()
#         for paragraph in document_text:
#             translation = self.translate_paragraph(paragraph)
#             messages.append({"role": "user", "content": paragraph})
#             messages.append({"role": "assistant", "content": translation})
#         return messages


    
#     def gpt_translate(self,user_message):
#         messages = self.system_prompt_message + user_message
#         response = self.client.chat.completions.create(messages=messages, model=self.model_name)
#         translation = response.choices[0].message.content
#         return translation    
    


#     def translate_paragraph(self, paragraph_text: str) -> str:
#         user_message = [{"role": "user", "content": paragraph_text}]        
#         self.validate_input(paragraph_text)
#         output_text = self.gpt_translate(user_message)
#         return self.normalize_output(paragraph_text,output_text)
    
#     def validate_input(self,paragraph_text:str):
#         user_message = [{"role": "user", "content": paragraph_text}]
#         # our use case already split the paragraphs into multiple chunks , no need to split the message
#         if estimate_tokens(user_message, functions=None, function_call=None) >= self.token_max_limit:
#             raise InvalidUserInputError('too much words', "יותר מידע מילים") # 
        
        
#         # prompt injection , there is libaries and stuff like this, do not implement this yourself.   (paragraph_text)
#         # here. raise InvalidUserInputError('dangerous text', "טקסט מסוכן") # 

        


    
    
#     def normalize_output(self,text_input:str,output_text:str):
#         # if the unintended output in not related to user input (which we theoreticly checked) , we still need to check that the output is intended.
#         # the understanding how to handle the errors comes from many unique tests.

#         # check by negatives, 
#         if not output_text.strip().lower().endswith(self.translation_success_string):
#             # output_text = handle_invalid_translation_string(output_text)
#             pass
#         else:
#             return output_text.replace(self.translation_success_string, '') # return or you can continue checking...

#         # check if they are APPROX same length , (maybe after removing 'a', 'is', etc...)
        
#         # depending on unintended output , a different handling is required


#         # retry is possible but only  if you change a bit the promot/ change the model / check if the output is different

#         return output_text








#     def normalized_translation(self,translation):
#         if self.validate_translation(translation):
#             return translation.replace(self.translation_success_string, '')
#         else:
#             logger.error(translation)
#             return "should not be here"




#     def validate_translation(self, translation_text: str) -> bool:
#         return True
#         return translation_text.strip().lower().endswith(self.translation_success_string)
        

#     def translate_para_example(text):
#         # input check
#         # check its not prompt injection,
#         # check prompt is actually hebrew , etc ...
#         # ...
#         # IF USER INPUT IS BAD -> raise Exception
#         output = text
#         # check output
#         # check specific keywords
#         # check if valid ,another model , might help , but not 100% 
#         # example check if the output and the input is approximily the same range / same number of words (after maybe removing the a, is , etc...)

#         # if output is invalid 
#         # retry / change prompt abit and retry / model change prompt retry
#         # 

#         # after model call
 
        
        


