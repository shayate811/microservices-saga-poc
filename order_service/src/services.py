from sqlalchemy.orm import Session
from . import models, schemas
import httpx
import os

# 決済サービスのURLを環境変数から取得 (docker-composeで設定済み)
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:8001")

# ==========================================
# DB操作 (CRUD)
# ==========================================

def create_order(db: Session, order: schemas.OrderCreate):
    """注文を 'PENDING' ステータスで作成する"""
    db_order = models.Order(
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price,
        status="PENDING" # 最初は保留中
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: str):
    """注文ステータスを更新する (COMPLETED / CANCELLED)"""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

# ==========================================
# 外部サービス連携 (Saga Orchestration)
# ==========================================

async def request_payment(order_id: int, amount: int):
    """決済サービスにHTTPリクエストを送る"""
    async with httpx.AsyncClient() as client:
        try:
            # Payment ServiceのAPIを叩く
            response = await client.post(
                f"{PAYMENT_SERVICE_URL}/payments/",
                json={"order_id": order_id, "amount": amount},
                timeout=5.0 # タイムアウト設定は必須
            )
            response.raise_for_status() # 200系以外なら例外を投げる
            return True
        except Exception as e:
            print(f"Payment failed: {e}")
            return False
