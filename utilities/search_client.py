from dotenv import load_dotenv
load_dotenv(override=True) 
import os, requests
from langchain_openai import AzureChatOpenAI
import json
from openai import AzureOpenAI
from azure.identity import ClientSecretCredential
from azure.search.documents import SearchClient

class Config:

    tenant_id = os.getenv("tenant_id")
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    kong_client_id=os.getenv("kong_client_id")
    kong_client_secret=os.getenv("kong_client_secret")
    kong_base_url=os.getenv("kong_base_url")
    api_version=os.getenv("api_version")
    api_deployment_name="gpt-4o"
    url = os.getenv("url")
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    azure_search_endpoint = os.getenv("azure_search_endpoint")
    azure_search_index = "testonepdf"

config = Config()

def get_search_client():
    spn_credential = ClientSecretCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )

    search_client = SearchClient(
            endpoint=config.azure_search_endpoint,
            index_name=config.azure_search_index,
            credential=spn_credential,
        )
    return search_client