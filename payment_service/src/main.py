from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import engine, get_db

# アプリ起動時にテーブルを自動作成 (簡易マイグレーション)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/payments/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # 【Zenn用演出】カオスエンジニアリング的な仕掛け
    # 金額が 9999 の時だけ、決済サービスのシステム障害をシミュレートする
    if payment.amount == 9999:
        print("💥 Payment System Crash Simulated!")
        raise HTTPException(status_code=500, detail="Payment System Error occurred!")

    return services.create_payment(db=db, payment=payment)
