# Dockerfile

# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt をコピーして必要なPythonパッケージをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトのソースコードをコピー
COPY . .

# エントリーポイントを設定
CMD ["python", "your_main_script.py"]