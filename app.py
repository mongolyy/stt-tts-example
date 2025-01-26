import streamlit as st
from streamlit_mic_recorder import mic_recorder
from langchain_openai import ChatOpenAI
import base64
import io
import subprocess
import tempfile
import os

st.title("文字起こしアプリ")

# 入力方法の選択
input_method = st.radio(
    "入力方法を選択してください",
    ["マイクで文字起こし", "音声ファイルをアップロード"]
)

if input_method == "マイクで文字起こし":
    st.write("🎤 以下のボタンをクリックして録音を開始/停止できます")
    
    # マイクレコーダーの表示
    audio = mic_recorder(
        start_prompt="録音開始",
        stop_prompt="録音停止",
        key="recorder"
    )
    
    if audio:
        # 音声データの取得
        st.audio(audio['bytes'])  # 録音した音声を再生可能に
        
        with st.spinner("文字を起こしています..."):
            # 一時ファイルの作成
            with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as webm_file:
                webm_file.write(audio['bytes'])
                webm_path = webm_file.name

            # WAVファイルのパス
            wav_path = webm_path.replace('.webm', '.wav')

            try:
                # WebMからWAVへの変換
                subprocess.run([
                    'ffmpeg', '-i', webm_path,
                    '-acodec', 'pcm_s16le',
                    '-ar', '16000',
                    '-ac', '1',
                    wav_path
                ], check=True)

                # WAVファイルの読み込みとbase64エンコード
                with open(wav_path, 'rb') as wav_file:
                    audio_bytes = wav_file.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()

                llm = ChatOpenAI(
                    model="gpt-4o-audio-preview",
                    temperature=0,
                )
                
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

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.error("エラーの詳細:")
                st.json(e.response.json() if hasattr(e, 'response') else str(e))

            finally:
                # 一時ファイルの削除
                try:
                    os.unlink(webm_path)
                    os.unlink(wav_path)
                except:
                    pass

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
                                {"type": "text", "text": "次の日本語の文章を文字起こししてください:"},
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
