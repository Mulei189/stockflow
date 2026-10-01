from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.categories.models import Category
from .models import Product
from .schemas import ProductResponse


# Create product
def create_product(payload, db: Session):

    data = payload.model_dump()

    # Validate category exists
    category = (
        db.query(Category)
        .filter(Category.id == data["category_id"])
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category not found"
        )

    # Check SKU
    existing_product = (
        db.query(Product)
        .filter(Product.sku == data["sku"])
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    product = Product(**data)

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "success": True,
        "product": ProductResponse.model_validate(product)
    }


# Get all products
def get_products(db: Session):
    products = db.query(Product).all()

    return {
        "success": True,
        "products": [
            ProductResponse.model_validate(product)
            for product in products
        ]
    }


# Get product by id
def get_product(db: Session, product_id: int):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "success": True,
        "product": ProductResponse.model_validate(product)
    }


# Update product
def update_product(db: Session, product_id: int, payload):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    data = payload.model_dump(exclude_unset=True)

    # Validate category if category_id is being changed
    if "category_id" in data:

        category = (
            db.query(Category)
            .filter(Category.id == data["category_id"])
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=400,
                detail="Category not found"
            )

    # Update product
    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {
        "success": True,
        "product": ProductResponse.model_validate(product)
    }


# Delete product
def delete_product(db: Session, product_id: int):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "success": True,
        "message": "Product deleted successfully"
    }