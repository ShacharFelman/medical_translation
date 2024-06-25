from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.chat_models  import ChatOllama
import os

api_key_openai = os.getenv('API_KEY_OPENAI')
api_key_anthropic = os.getenv('API_KEY_ANTHROPIC')
api_key_google_genai = os.getenv('API_KEY_GOOGLE_GENAI')
ollama_container_name = 'MediTranslateAI-ollama'
ollama_container_url = f'http://{ollama_container_name}:11434'

def initialize_llms():
    gpt_4o = ChatOpenAI(model_name='gpt-4o',
                            temperature=0.0,
                            api_key=api_key_openai)
    
    claude_3_opus = ChatAnthropic(model_name='claude-3-opus-20240229',
                                  temperature=0.0,
                                  api_key=api_key_anthropic)
    
    gemini_pro = ChatGoogleGenerativeAI(model='gemini-pro',
                                  temperature=0.0,
                                  google_api_key=api_key_google_genai)

    llama3 = ChatOllama(base_url=ollama_container_url,
                            model="llama3",
                            temperature=0.0)

    phi3 = ChatOllama(base_url=ollama_container_url,
                        model="phi3",
                        temperature=0.0)

    aya = ChatOllama(base_url=ollama_container_url,
                            model="aya",
                            temperature=0.0)
    
    gemma = ChatOllama(base_url=ollama_container_url,
                            model="gemma",
                            temperature=0.0)
    
    qwen2 = ChatOllama(base_url=ollama_container_url,
                            model="qwen2",
                            temperature=0.0)
    
    return [
            gpt_4o
            ,claude_3_opus
            ,gemini_pro
            # llama3
            # ,phi3
            # ,aya
            # ,gemma
            # ,qwen2
            ]