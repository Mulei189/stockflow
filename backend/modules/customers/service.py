from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Customer
from .schemas import CustomerResponse


def create_customer(payload, db: Session):

    data = payload.model_dump()

    # Check if email already exists
    if data.get("email"):
        existing_customer = (
            db.query(Customer)
            .filter(Customer.email == data["email"])
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer email already exists"
            )

    customer = Customer(**data)

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {
        "success": True,
        "message": "Customer created successfully",
        "customer": CustomerResponse.model_validate(customer)
    }


def get_customers(db: Session):

    customers = db.query(Customer).all()

    return {
        "success": True,
        "message": "Customers retrieved successfully",
        "count": len(customers),
        "customers": [
            CustomerResponse.model_validate(customer)
            for customer in customers
        ]
    }


def get_customer(db: Session, customer_id: int):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "success": True,
        "customer": CustomerResponse.model_validate(customer)
    }


def update_customer(db: Session, customer_id: int, payload):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    data = payload.model_dump(exclude_unset=True)

    # Check email uniqueness if email is being changed
    if data.get("email"):
        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.email == data["email"],
                Customer.id != customer_id
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer email already exists"
            )

    for key, value in data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return {
        "success": True,
        "message": "Customer updated successfully",
        "customer": CustomerResponse.model_validate(customer)
    }


def delete_customer(db: Session, customer_id: int):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "success": True,
        "message": "Customer deleted successfully"
    }