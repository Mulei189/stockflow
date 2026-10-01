from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db

from modules.purchases.schema import (
    PurchaseCreate,
    PurchaseResponse
)

from modules.purchases.service import (
    create_purchase,
    get_purchase_by_id,
    get_purchases
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_purchase(
    payload: PurchaseCreate,
    db: Session = Depends(get_db)
):
    return create_purchase(payload, db)

@router.get(
    "/",
    response_model=list[PurchaseResponse]
)
def get_all_purchases(
    db: Session = Depends(get_db)
):
    return get_purchases(db)

@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    return get_purchase_by_id(purchase_id, db)