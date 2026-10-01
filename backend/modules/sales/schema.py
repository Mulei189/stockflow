from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    customer_id: int
    items: list[SaleItemCreate]


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    customer_id: int
    total_amount: Decimal
    status: str
    sale_date: datetime
    created_at: datetime
    items: list[SaleItemResponse]

    class Config:
        from_attributes = True