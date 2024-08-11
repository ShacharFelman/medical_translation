from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models  import ChatOllama

from services.translation.translator_llm import TranslatorLLM
import os

api_key_openai = os.getenv('API_KEY_OPENAI')
api_key_anthropic = os.getenv('API_KEY_ANTHROPIC')
api_key_google_genai = os.getenv('API_KEY_GOOGLE_GENAI')
ollama_url = 'http://host.docker.internal:11434'

def initialize_translators():
    gpt_4o = ChatOpenAI(model_name='gpt-4o',
                        temperature=0.0,
                        api_key=api_key_openai)
    

    gpt_4_turbo = ChatOpenAI(model_name='gpt-4-turbo',
                        temperature=0.0,
                        api_key=api_key_openai)

    claude_3_opus = ChatAnthropic(model_name='claude-3-opus-20240229',
                                  temperature=0.0,
                                  api_key=api_key_anthropic)
    
    claude_35_sonnet = ChatAnthropic(model_name='claude-3-5-sonnet-20240620',
                                temperature=0.0,
                                api_key=api_key_anthropic)
    
    # qwen2 = ChatOllama(base_url=ollama_url,
    #                     model="qwen2:1.5b",
    #                     temperature=0.0)

    return [
        # TranslatorLLM(gpt_4_turbo, 'gpt-4-turbo'),
        TranslatorLLM(claude_3_opus, 'claude-3-opus'),
        TranslatorLLM(gpt_4o, 'gpt-4o'),
        TranslatorLLM(claude_35_sonnet, 'claude-3-5-sonnet'),
    ]