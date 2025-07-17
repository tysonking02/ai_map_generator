from auth import auth
from build_system_prompt import build_system_prompt
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

# endpoint = "https://map-generator-poc-resource.services.ai.azure.com/models"
# model_name = "Llama-4-Maverick-17B-128E-Instruct-FP8"

endpoint = "https://map-generator-poc-resource.cognitiveservices.azure.com/"
deployment = "o4-mini"

client = auth()
system_prompt = build_system_prompt()

def request_response(user_input):
    response = client.chat.completions.create(
        model=deployment,  # This is your deployment name
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_completion_tokens=2048,
    )

    return response.choices[0].message.content