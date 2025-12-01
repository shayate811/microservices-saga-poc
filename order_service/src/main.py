from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import engine, get_db

# テーブル自動作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 1. ローカルTX: まず自分のDBに「PENDING」で書き込む
    # ここでコミットされるため、後でエラーが起きてもこのレコードは消えない！(不整合の始まり)
    new_order = services.create_order(db=db, order=order)
    
    # 2. 外部サービス呼び出し: 決済サービスへリクエスト
    # ここでネットワーク遅延や相手のダウンが発生する可能性がある
    payment_success = await services.request_payment(order_id=new_order.id, amount=order.price)
    
    # 3. Sagaロジック: 結果に応じた事後処理
    if payment_success:
        # 成功時: ステータスを完了にする
        services.update_order_status(db, new_order.id, "COMPLETED")
    else:
        # 失敗時: ここが超重要！
        # これを書かないと「商品は確保したのに金が払われていない」状態になる
        # これを「補償トランザクション (Compensating Transaction)」と呼ぶ
        # services.update_order_status(db, new_order.id, "CANCELLED")
        
        raise HTTPException(status_code=400, detail="Payment failed, Order cancelled")
        
    return new_order
