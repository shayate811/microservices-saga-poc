from sqlalchemy import Column, Integer, String
from .database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    
    # 他のマイクロサービス(Order)のIDを持ちますが、
    # 外部キー制約(ForeignKey)は付けません！これぞ疎結合。
    order_id = Column(Integer, index=True)
    
    amount = Column(Integer)
    
    # PAID(支払済) or FAILED(失敗) or REFUNDED(返金済)
    status = Column(String, default="PENDING")
