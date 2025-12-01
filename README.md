```
microservices-saga-poc/
├── docker-compose.yml          # 全体の構成定義（ここが司令塔）
├── README.md                   # Zenn記事のネタ帳にもなる
│
├── order_service/              # 【注文サービス】（在庫管理）
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # FastAPIのエントリーポイント
│       ├── models.py           # DB定義 (SQLAlchemyなど)
│       ├── schemas.py          # リクエスト/レスポンス定義 (Pydantic)
│       ├── database.py         # DB接続設定
│       └── services.py         # ビジネスロジック
│
└── payment_service/            # 【決済サービス】（残高管理）
    ├── Dockerfile
    ├── requirements.txt
    └── src/
        ├── main.py
        ├── models.py
        ├── ... (Orderと同じ構造)
```
