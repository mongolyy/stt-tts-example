# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このリポジトリは、OpenAI GPT-4のAudioモデルを使用した音声文字起こし（Speech-to-Text）Webアプリケーションです。
StreamlitによるWebUIを提供し、マイクからのリアルタイム録音と音声ファイルアップロードの両方に対応しています。

## 開発環境セットアップ

### 必要要件
- Python 3.13以上
- uv (パッケージマネージャー)
- ffmpeg (音声変換用)
- OpenAI APIキー

### 環境構築
```bash
# 依存関係のインストール
uv sync

# 環境変数設定
cp .env.example .env
# .envファイルでOPENAI_API_KEYなどを設定
```

### アプリケーション起動
```bash
export UV_ENV_FILE=.env
streamlit run app.py
```

## プロジェクト構造

- `app.py` - メインのStreamlitアプリケーション
- `test_whisper.py` - 音声文字起こしのテスト用スクリプト
- `pyproject.toml` - uv用の依存関係定義
- `sample.mp3` - テスト用音声ファイル

## 技術スタック

### 依存関係
- `streamlit` - WebUIフレームワーク
- `streamlit-mic-recorder` - マイク録音機能
- `langchain-openai` - OpenAI APIとの接続（OpenAI・Azure OpenAI両対応）
- `langchain-community`, `langchain-core` - LangChainエコシステム

### 音声処理フロー
1. マイク録音: WebM形式で録音 → ffmpegでWAV変換
2. ファイルアップロード: MP3形式を直接処理
3. 文字起こし: OpenAI GPT-4o-audio-previewモデルまたはAzure OpenAIを使用
4. 音声データはbase64エンコードしてAPIに送信

### LLMプロバイダー
- OpenAI: GPT-4o-audio-previewモデル
- Azure OpenAI: 任意のデプロイメント名を指定可能

## 開発時の注意事項

- マイク録音時は一時ファイルを作成し、処理後に削除
- 音声変換にはffmpegが必要
- OpenAI APIの利用には課金が発生
- 現在のマイク録音はWebM形式のみ対応
- ファイルアップロードは現在MP3形式のみ対応

## テスト実行

```bash
# 単体テスト実行
python test_whisper.py
```

## 環境変数

### OpenAI用
- `OPENAI_API_KEY` - OpenAI APIキー

### Azure OpenAI用
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAIエンドポイント
- `AZURE_OPENAI_API_KEY` - Azure OpenAI APIキー
- `AZURE_OPENAI_API_VERSION` - APIバージョン（デフォルト: 2025-01-01-preview）
- `AZURE_OPENAI_DEPLOYMENT_NAME` - デプロイメント名

### LangSmith用（オプション）
- `LANGSMITH_TRACING` - LangSmithトレース有効化
- `LANGSMITH_API_KEY` - LangSmith APIキー
- `LANGSMITH_PROJECT` - LangSmithプロジェクト名