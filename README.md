# Speech-to-Text アプリケーション

リアルタイムの音声文字起こしが可能なWebアプリケーションです。マイクからの直接入力または音声ファイルのアップロードに対応しており、OpenAI GPT-4のAudioモデルを使用して高精度な文字起こしを実現します。

## 主な機能

- 🎤 マイクを使用したリアルタイム音声録音と文字起こし
- 📁 音声ファイル（MP3）のアップロードによる文字起こし
- 🔊 録音した音声の再生機能
- 🇯🇵 日本語の音声に対応

## 必要要件

- Python 3.13以上
- ffmpeg（音声変換用）
- OpenAI APIキー
- LangSmith API設定（オプション）
- uv（パッケージマネージャー）

## インストール手順

1. リポジトリのクローン:
```sh
git clone [リポジトリURL]
cd stt-tts-example
```

2. 依存パッケージのインストール:
```sh
uv sync
```

3. ffmpegのインストール:
- Windows: wingetを使用してインストール
```sh
winget install Gyan.FFmpeg
```
- macOS: Homebrewを使用してインストール
```sh
brew install ffmpeg
```

## 環境設定

1. `.env.example`を`.env`にコピー:
```sh
cp .env.example .env
```

2. `.env`ファイルを編集し、必要な環境変数を設定:
```
OPENAI_API_KEY="your-api-key-here"
LANGSMITH_TRACING="true"  # オプション
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"  # オプション
LANGSMITH_API_KEY="your-langsmith-api-key"  # オプション
LANGSMITH_PROJECT="your-project-name"  # オプション
```

## 使用方法

1. アプリケーションの起動:
```sh
streamlit run app.py
```

2. ブラウザで`http://localhost:8501`を開く

3. 入力方法を選択:
   - 「マイクでリアルタイム文字起こし」: マイクボタンをクリックして録音を開始/停止
   - 「音声ファイルをアップロード」: MP3ファイルをドラッグ&ドロップまたは選択

4. 文字起こし結果が画面に表示されます

## 注意事項

- マイクでの録音時は、ブラウザがマイクへのアクセスを要求します。許可してください。
- 音声ファイルのアップロードは現在MP3形式のみ対応しています。
- OpenAI APIの利用には課金が発生する可能性があります。
