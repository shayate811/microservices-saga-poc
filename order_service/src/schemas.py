from pydantic import BaseModel

# 共通のベースクラス
class OrderBase(BaseModel):
    item_name: str
    quantity: int
    price: int

# 作成時（リクエスト）にはステータスやIDは不要
class OrderCreate(OrderBase):
    pass

# 応答時（レスポンス）にはIDとステータスを含める
class Order(OrderBase):
    id: int
    status: str

    # SQLAlchemyのモデルをPydanticモデルに変換するための魔法の設定
    class Config:
        from_attributes = True
