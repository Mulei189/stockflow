from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.stock_movements.models import StockMovement


def create_stock_movement(
    db: Session,
    product_id: int,
    movement_type: str,
    quantity: int,
    reference_type: str | None = None,
    reference_id: int | None = None,
    notes: str | None = None
):
    movement = StockMovement(
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        notes=notes
    )

    db.add(movement)

    return movement


def get_stock_movements(db: Session):
    return (
        db.query(StockMovement)
        .order_by(StockMovement.id.desc())
        .all()
    )


def get_stock_movement_by_id(
    movement_id: int,
    db: Session
):
    movement = (
        db.query(StockMovement)
        .filter(StockMovement.id == movement_id)
        .first()
    )

    if not movement:
        raise HTTPException(
            status_code=404,
            detail="Stock movement not found"
        )

    return movement

def get_product_stock_movements(
    product_id: int,
    db: Session
):
    return (
        db.query(StockMovement)
        .filter(StockMovement.product_id == product_id)
        .order_by(StockMovement.id.desc())
        .all()
    )