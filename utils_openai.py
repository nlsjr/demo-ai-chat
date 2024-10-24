import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import AzureChatOpenAI

_ = load_dotenv(find_dotenv())

openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')


def get_response(historic_message):
    llm = AzureChatOpenAI(
        azure_endpoint=openai_endpoint,
        api_key=api_key,
        azure_deployment="gpt-4o",  # or your deployment
        api_version=api_version,  # or your api version
        temperature=0.2,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    formatted_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who responds to the user in a straightforward and efficient manner."
        }
    ]

    for messages in historic_message:
        formatted_messages.append(
            {
                'role': messages['role'],
                'content': messages['content']
            }
        )

    ai_msg = llm.invoke(formatted_messages)

    return {
        'role': "ai",
        'content': ai_msg.content
    }
