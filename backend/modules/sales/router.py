from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db

from modules.sales.schema import SaleCreate, SaleResponse
from modules.sales.service import (
    create_sale,
    get_sales,
    get_sale_by_id,
)


router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_sale(
    payload: SaleCreate,
    db: Session = Depends(get_db)
):
    return create_sale(payload, db)


@router.get(
    "/",
    response_model=list[SaleResponse]
)
def get_all_sales(
    db: Session = Depends(get_db)
):
    return get_sales(db)


@router.get(
    "/{sale_id}",
    response_model=SaleResponse
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    return get_sale_by_id(sale_id, db)