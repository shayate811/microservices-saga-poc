from sqlalchemy.orm import Session
from . import models, schemas

def create_payment(db: Session, payment: schemas.PaymentCreate):
    # 1. 支払い情報の作成
    # ここに「金額が足りているか？」などのビジネスロジックが入る想定
    db_payment = models.Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        status="PAID"  # 正常系として一旦PAIDで登録
    )
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    return db_payment
