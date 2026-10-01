from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.products.models import Product

def get_stock_status(quantity: int, threshold: int):
    if quantity == 0:
        return "OUT_OF_STOCK"

    if quantity <= threshold:
        return "LOW_STOCK"

    return "IN_STOCK"

def get_inventory(db: Session):
    products = (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )
    
    inventory = []
    
    for product in products:
        stock_value = product.quantity * product.price
        
        inventory.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "quantity": product.quantity,
            "price": product.price,
            "stock_value": stock_value,
            "low_stock_threshold": product.low_stock_threshold,
            "stock_status": get_stock_status(
                product.quantity,
                product.low_stock_threshold
            ),
        })
    
    return inventory

def get_inventory_item(product_id: int, db: Session):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    stock_value = product.quantity * product.price
    
    return {
        "product_id": product.id,
        "product_name": product.name,
        "sku": product.sku,
        "quantity": product.quantity,
        "price": product.price,
        "stock_value": stock_value,
        "low_stock_threshold": product.low_stock_threshold,
        "stock_status": get_stock_status(
            product.quantity,
            product.low_stock_threshold
        ),
    }
    
def get_inventory_summary(db: Session):
    products = db.query(Product).all()

    total_products = len(products)

    total_units = sum(
        product.quantity for product in products
    )

    total_stock_value = sum(
        product.quantity * product.price
        for product in products
    )

    return {
        "total_products": total_products,
        "total_units": total_units,
        "total_stock_value": total_stock_value,
    }
    
def get_low_stock_products(db: Session):
    products = (
        db.query(Product)
        .filter(
            Product.quantity > 0,
            Product.quantity <= Product.low_stock_threshold
        )
        .order_by(Product.quantity.asc())
        .all()
    )

    inventory = []

    for product in products:
        inventory.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "quantity": product.quantity,
                "unit_price": product.price,
                "stock_value": product.quantity * product.price,
                "low_stock_threshold": product.low_stock_threshold,
                "stock_status": "LOW_STOCK",
            }
        )

    return inventory

def get_out_of_stock_products(db: Session):
    products = (
        db.query(Product)
        .filter(Product.quantity == 0)
        .order_by(Product.id.asc())
        .all()
    )

    inventory = []

    for product in products:
        inventory.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "quantity": product.quantity,
                "unit_price": product.price,
                "stock_value": product.quantity * product.price,
                "low_stock_threshold": product.low_stock_threshold,
                "stock_status": "OUT_OF_STOCK",
            }
        )

    return inventory