from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from modules.inventory.schema import (
    InventoryItemResponse,
    InventorySummaryResponse,
)

from modules.inventory.service import (
    get_inventory,
    get_inventory_item,
    get_inventory_summary,
    get_low_stock_products,
    get_out_of_stock_products,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get(
    "/",
    response_model=list[InventoryItemResponse]
)
def get_all_inventory(
    db: Session = Depends(get_db)
):
    return get_inventory(db)


@router.get(
    "/summary",
    response_model=InventorySummaryResponse
)
def get_inventory_summary_data(
    db: Session = Depends(get_db)
):
    return get_inventory_summary(db)

@router.get(
    "/low-stock",
    response_model=list[InventoryItemResponse]
)
def get_low_stock_inventory(
    db: Session = Depends(get_db)
):
    return get_low_stock_products(db)


@router.get(
    "/out-of-stock",
    response_model=list[InventoryItemResponse]
)
def get_out_of_stock_inventory(
    db: Session = Depends(get_db)
):
    return get_out_of_stock_products(db)

@router.get(
    "/{product_id}",
    response_model=InventoryItemResponse
)
def get_inventory_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_inventory_item(product_id, db)