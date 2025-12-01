# 1. ベースイメージ: 軽量なslim版を使用 (AlpineはPythonと相性悪い場合があるためslim推奨)
FROM python:3.11-slim

# 2. 作業ディレクトリの設定
WORKDIR /app

# 3. 依存関係のインストール
# ポイント: ソースコードより先にrequirements.txtだけをコピーする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. ソースコードのコピー
COPY . .

# 5. ポートの公開 (ドキュメントとしての意味合いが強い)
EXPOSE 8000 8001
