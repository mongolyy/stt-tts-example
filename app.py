import base64
import streamlit as st
from langchain_openai import ChatOpenAI

st.title("音声文字起こしアプリ")

audio_file = st.file_uploader("音声ファイルをアップロードしてください", type=["mp3"])

if audio_file is not None:
    st.audio(audio_file, format="audio/mp3")

    if st.button("文字起こしを実行する"):
        with st.spinner("文字を起こしています..."):
            
            llm = ChatOpenAI(
                model="gpt-4o-audio-preview",
                temperature=0,
            )

            audio = audio_file.read()
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
            st.success("文字起こし完了しました！")
            st.write(output_message.content)

            
