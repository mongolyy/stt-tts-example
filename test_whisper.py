import base64
import os
from langchain_openai import ChatOpenAI, AzureChatOpenAI

def create_llm():
    # Azure OpenAIの設定が存在するかチェック
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0,
        )
    else:
        return ChatOpenAI(
            model="gpt-4o-audio-preview",
            temperature=0,
        )

llm = create_llm()

with open(
    "./sample.mp3",
    "rb"
) as f:
    audio = f.read()
    audio_base64 = base64.b64encode(audio).decode()

output_message = llm.invoke(
    [
        (
            "human",
            [
                {"type": "text", "text": "Transcribe the following:"},
                {
                    "type": "input_audio",
                    "input_audio": {"data": audio_base64, "format": "mp3"},
                },
            ],
        ),
    ]
)
print(output_message.content)
