from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_cost: Decimal = Field(gt=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    items: list[PurchaseItemCreate]


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_cost: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    total_amount: Decimal
    status: str
    purchase_date: datetime
    created_at: datetime
    items: list[PurchaseItemResponse]

    class Config:
        from_attributes = True