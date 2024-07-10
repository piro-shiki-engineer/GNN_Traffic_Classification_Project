# ベースイメージ
FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# 環境変数を設定
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# requirements.txt をコピーして必要なPythonパッケージをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# PyTorch Geometricの依存関係を個別にインストール
RUN pip install --no-cache-dir torch-scatter==2.0.9 -f https://data.pyg.org/whl/torch-1.10.0+cu113.html
RUN pip install --no-cache-dir torch-sparse==0.6.12 -f https://data.pyg.org/whl/torch-1.10.0+cu113.html
RUN pip install --no-cache-dir torch-cluster==1.5.9 -f https://data.pyg.org/whl/torch-1.10.0+cu113.html
RUN pip install --no-cache-dir torch-spline-conv==1.2.1 -f https://data.pyg.org/whl/torch-1.10.0+cu113.html
RUN pip install --no-cache-dir torch-geometric==2.0.3

# プロジェクトのソースコードをコピー
COPY . .

# コンテナが終了しないように設定
CMD ["tail", "-f", "/dev/null"]