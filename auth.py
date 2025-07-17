from openai import AzureOpenAI
import os
import streamlit as st
from dotenv import load_dotenv

def auth():
    load_dotenv()
    api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY")

    client = AzureOpenAI(
        azure_endpoint="https://map-generator-poc-resource.openai.azure.com/", 
        api_key=api_key,
        api_version="2024-12-01-preview"
    )

    return client