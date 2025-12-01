from sqlalchemy import Column, Integer, String
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Integer)
    
    # ここが重要: 注文のステータス遷移を観察します
    # PENDING(保留) -> COMPLETED(完了) or CANCELLED(補償TXで取消)
    status = Column(String, default="PENDING")
