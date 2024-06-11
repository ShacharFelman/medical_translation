from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os

api_key_openai = os.getenv('API_KEY_OPENAI')
api_key_anthropic = os.getenv('API_KEY_ANTHROPIC')

def initialize_llms():
    openai_llm = ChatOpenAI(model_name='gpt-4o',
                            temperature=0.0,
                            api_key=api_key_openai)
    
    anthropic_llm = ChatAnthropic(model_name='claude-3-opus-20240229',
                                  temperature=0.0,
                                  api_key=api_key_anthropic)
    
    return [openai_llm, anthropic_llm]