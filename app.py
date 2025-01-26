import base64
import io
import streamlit as st
from langchain_openai import ChatOpenAI
from audio_recorder_streamlit import audio_recorder

st.title("音声文字起こしアプリ")

# 入力方法の選択
input_method = st.radio(
    "入力方法を選択してください",
    ["マイクで録音", "音声ファイルをアップロード"]
)

if input_method == "マイクで録音":
    # マイクからの録音
    st.write("🎤 以下のボタンをクリックして録音を開始/停止できます")
    audio_bytes = audio_recorder(pause_threshold=3)
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        if st.button("録音した音声を文字起こし"):
            with st.spinner("文字を起こしています..."):
                llm = ChatOpenAI(
                    model="gpt-4o-audio-preview",
                    temperature=0,
                )
                
                # WAVをbase64エンコード
                audio_base64 = base64.b64encode(audio_bytes).decode()
                
                output_message = llm.invoke(
                    [
                        (
                            "human",
                            [
                                {"type": "text", "text": "次の日本語の文章を文字起こししてください:"},
                                {
                                    "type": "input_audio",
                                    "input_audio": {"data": audio_base64, "format": "wav"},
                                },
                            ],
                        ),
                    ]
                )
                st.success("文字起こし完了しました！")
                st.write(output_message.content)

else:
    # ファイルアップロード
    audio_file = st.file_uploader("音声ファイルをアップロードしてください", type=["mp3"])
    
    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3")
        
        if st.button("アップロードした音声を文字起こし"):
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
