from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from .schemas import CreateSupplierSchema, UpdateSupplierSchema
from .service import (
    create_supplier,
    get_suppliers,
    get_supplier,
    update_supplier,
    delete_supplier
)

router = APIRouter(
    prefix="/api/suppliers",
    tags=["Suppliers"]
)

@router.post("/", summary="Create a new supplier")
def create_supplier_endpoint(
    payload: CreateSupplierSchema,
    db: Session = Depends(get_db)
):
    return create_supplier(payload, db)

@router.get("/", summary="Get all suppliers")
def get_suppliers_endpoint(
    db: Session = Depends(get_db)
):
    return get_suppliers(db)

@router.get("/{supplier_id}", summary="Get a supplier by ID")
def get_supplier_endpoint(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    return get_supplier(db, supplier_id)

@router.put("/{supplier_id}", summary="Update a supplier by ID")
def update_supplier_endpoint(
    supplier_id: int,
    payload: UpdateSupplierSchema,
    db: Session = Depends(get_db)
):
    return update_supplier(db, supplier_id, payload)

@router.delete("/{supplier_id}", summary="Delete a supplier by ID")
def delete_supplier_endpoint(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    return delete_supplier(db, supplier_id)