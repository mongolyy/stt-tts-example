import base64
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-audio-preview",
    temperature=0,
)

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
