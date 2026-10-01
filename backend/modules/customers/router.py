from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from .schemas import (
    CreateCustomerSchema,
    UpdateCustomerSchema
)

from .service import (
    create_customer,
    get_customers,
    get_customer,
    update_customer,
    delete_customer
)


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)


@router.post("/")
def create_customer_endpoint(
    payload: CreateCustomerSchema,
    db: Session = Depends(get_db)
):
    return create_customer(payload, db)


@router.get("/")
def get_customers_endpoint(
    db: Session = Depends(get_db)
):
    return get_customers(db)


@router.get("/{customer_id}")
def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return get_customer(db, customer_id)


@router.patch("/{customer_id}")
def update_customer_endpoint(
    customer_id: int,
    payload: UpdateCustomerSchema,
    db: Session = Depends(get_db)
):
    return update_customer(db, customer_id, payload)


@router.delete("/{customer_id}")
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return delete_customer(db, customer_id)