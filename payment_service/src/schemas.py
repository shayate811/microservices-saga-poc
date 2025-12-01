from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    amount: int

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: str

    class Config:
        from_attributes = True
