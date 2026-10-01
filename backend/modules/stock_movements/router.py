from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from modules.stock_movements.schema import StockMovementResponse

from modules.stock_movements.service import (
    get_product_stock_movements,
    get_stock_movements,
    get_stock_movement_by_id
)


router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)


@router.get(
    "/",
    response_model=list[StockMovementResponse]
)
def get_all_stock_movements(
    db: Session = Depends(get_db)
):
    return get_stock_movements(db)

@router.get(
    "/product/{product_id}",
    response_model=list[StockMovementResponse]
)
def get_product_movements(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product_stock_movements(
        product_id,
        db
    )

@router.get(
    "/{movement_id}",
    response_model=StockMovementResponse
)
def get_stock_movement(
    movement_id: int,
    db: Session = Depends(get_db)
):
    return get_stock_movement_by_id(
        movement_id,
        db
    )
    