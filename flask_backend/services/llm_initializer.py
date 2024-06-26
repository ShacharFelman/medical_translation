from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from services.translator import Translator
import os

api_key_openai = os.getenv('API_KEY_OPENAI')
api_key_anthropic = os.getenv('API_KEY_ANTHROPIC')
api_key_google_genai = os.getenv('API_KEY_GOOGLE_GENAI')

def initialize_translators():
    gpt_4o = ChatOpenAI(model_name='gpt-4o',
                        temperature=0.0,
                        api_key=api_key_openai)
    
    claude_3_opus = ChatAnthropic(model_name='claude-3-opus-20240229',
                                  temperature=0.0,
                                  api_key=api_key_anthropic)
    
    gemini_pro = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                                        temperature=0.0,
                                        google_api_key=api_key_google_genai)
    
    return [
        Translator(gpt_4o),
        Translator(claude_3_opus),
        Translator(gemini_pro)
    ]