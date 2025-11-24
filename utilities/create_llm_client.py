from dotenv import load_dotenv
load_dotenv(override=True) 
import os, requests
from langchain_openai import AzureChatOpenAI
import json
from openai import AzureOpenAI

class Config:
    kong_client_id=os.getenv("kong_client_id")
    kong_client_secret=os.getenv("kong_client_secret")
    kong_base_url=os.getenv("kong_base_url")
    api_version=os.getenv("api_version")
    api_deployment_name=os.getenv("api_deployment_name")
    url =os.getenv("url")
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    

config = Config()

def get_kong_token_with_client_id_and_client_secret(client_id, client_secret):
    # Endpoint URL
    # url = os.getenv("KONG_ENDPOINT_URL")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    # Data payload
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'openid email profile'
    }
    # Make a POST request
    response = requests.post(config.url, headers=headers, data=data)
    #if response fails 
    if not response.ok:
        # Print response status code and content if something went wrong
        print(f"Error: {response.status_code}")
        print(response.text)
    # Check if the request was successful
    if response.ok:
        dict_of_response_text=json.loads(response.text)
        return dict_of_response_text["access_token"]
    

def create_llm_client():
    bearer_access_token = get_kong_token_with_client_id_and_client_secret(client_id =config.kong_client_id, 
                                                          client_secret=config.kong_client_secret)
    llm = AzureChatOpenAI(
    temperature= 0,
    api_version=config.api_version,
    azure_endpoint=config.kong_base_url,
    azure_ad_token=bearer_access_token,
    model=config.api_deployment_name
    )
    return llm

def get_embedding(query):

    embedding_client = AzureOpenAI(
    api_version=config.api_version,
    azure_endpoint=config.kong_base_url,
    azure_ad_token=get_kong_token_with_client_id_and_client_secret(
        config.kong_client_id, config.kong_client_secret),)
    
    emb = embedding_client.embeddings.create(
        model=config.embedding_model,
        input=query
    ).data[0].embedding

    return emb
