from datetime import datetime
from pydantic import BaseModel


class StockMovementBase(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: int
    reference_type: str | None = None
    reference_id: int | None = None
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockMovementResponse(StockMovementBase):
    pass