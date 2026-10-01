from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Supplier
from .schemas import SupplierResponse

# Create a new supplier
def create_supplier(payload, db: Session):
    data = payload.model_dump()
    
    # Check if a supplier with the same name already exists
    existing_supplier = (
        db.query(Supplier)
        .filter(Supplier.name == data["name"])
        .first()
    )
    
    if existing_supplier:
        raise HTTPException(
            status_code=400,
            detail=f"Supplier with name '{data['name']}' already exists."
        )
    
    # Create a new supplier instance
    supplier = Supplier(**data)
    
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    
    return {
        "success": True,
        "message": "Supplier created successfully.",
        "supplier": SupplierResponse.model_validate(supplier)
    }

# Get all suppliers
def get_suppliers(db: Session):
    suppliers = db.query(Supplier).all()
    
    return {
        "success": True,
        "message": "Suppliers retrieved successfully.",
        "count": len(suppliers),
        "suppliers": [
            SupplierResponse.model_validate(supplier)
            for supplier in suppliers
        ]
    }

# Get a supplier by ID
def get_supplier(db: Session, supplier_id: int):
    
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )
    
    if not supplier:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID '{supplier_id}' not found."
        )
    
    return {
        "success": True,
        "supplier": SupplierResponse.model_validate(supplier)
    }

# Update a supplier by ID
def update_supplier(db: Session, supplier_id: int, payload):
    
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )
    
    if not supplier:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID '{supplier_id}' not found."
        )
    
    data = payload.model_dump(exclude_unset=True)
    
    # update the supplier instance with the new data
    for key, value in data.items():
        setattr(supplier, key, value)
        
    db.commit()
    db.refresh(supplier)
    
    return {
        "success": True,
        "message": "Supplier updated successfully.",
        "supplier": SupplierResponse.model_validate(supplier)
    }

# Delete a supplier by ID
def delete_supplier(db: Session, supplier_id: int):
    
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )
    
    if not supplier:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID '{supplier_id}' not found."
        )
    
    db.delete(supplier)
    db.commit()
    
    return {
        "success": True,
        "message": "Supplier deleted successfully."
    }
    