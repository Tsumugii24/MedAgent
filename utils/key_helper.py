import os
from dotenv import load_dotenv, find_dotenv
                                                                                                                                    
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_openai_base_url():
    load_env()
    openai_base_url = os.getenv("OPENAI_BASE_URL")
    return openai_base_url

def get_azure_openai_api_key():
    load_env()
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    return azure_openai_api_key

def get_azure_openai_endpoint():
    load_env()
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    return azure_openai_endpoint

def get_gpt4_api_key():
    load_env()
    gpt4_api_key = os.getenv("GPT4_API_KEY")
    return gpt4_api_key

def get_gpt4_base_url():
    load_env()
    gpt4_base_url = os.getenv("GPT4_BASE_URL")
    return gpt4_base_url