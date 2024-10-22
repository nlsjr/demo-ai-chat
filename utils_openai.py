from langchain_openai import AzureChatOpenAI

endpoint = "https://cognaai-west-us.openai.azure.com"
openai_api_key = "a2e32b70b6964cb9bc8f37204e397854"
openai_api_version = "2024-02-15-preview"


def get_response(historic_message, stream=False):
    llm = AzureChatOpenAI(
        azure_endpoint=endpoint,
        api_key=openai_api_key,
        azure_deployment="gpt-4o",  # or your deployment
        api_version=openai_api_version,  # or your api version
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
