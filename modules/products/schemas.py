from typing import Optional

from pydantic import BaseModel, Field
from decimal import Decimal

class CreateProductSchema(BaseModel):
    name: str
    sku: str
    description: str | None = None
    price: Decimal = Field(gt=0)
    quantity: int = Field(default=0, ge=0)
    category_id: int
    low_stock_threshold: int = Field(default=5, gt=0)

class UpdateProductSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)
    category_id: Optional[int] = None
    low_stock_threshold: int | None = Field(default=None, gt=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None = None
    price: Decimal
    quantity: int
    low_stock_threshold: int

    class Config:
        from_attributes = True