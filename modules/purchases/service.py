from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.purchases.model import Purchase, PurchaseItem
from modules.purchases.schema import PurchaseCreate
from modules.suppliers.models import Supplier
from modules.products.models import Product

from modules.stock_movements.service import create_stock_movement

def create_purchase(payload: PurchaseCreate, db: Session):
    # 1. Check supplier
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == payload.supplier_id)
        .first()
    )

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    # Prevent empty purchases
    if not payload.items:
        raise HTTPException(
            status_code=400,
            detail="Purchase must contain at least one item"
        )

    total_amount = 0
    purchase_items = []

    # 2. Validate products and prepare items
    for item in payload.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {item.product_id} not found"
            )

        subtotal = item.quantity * item.unit_cost
        total_amount += subtotal

        purchase_item = PurchaseItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
            subtotal=subtotal
        )

        purchase_items.append(
            (purchase_item, product)
        )

    # 3. Create purchase
    purchase = Purchase(
        supplier_id=payload.supplier_id,
        total_amount=total_amount,
        status="received"
    )

    try:
        db.add(purchase)
        db.flush()

        # 4. Add items and update stock
        for purchase_item, product in purchase_items:

            purchase_item.purchase_id = purchase.id

            db.add(purchase_item)

            product.quantity += purchase_item.quantity

            create_stock_movement(
                db=db,
                product_id=product.id,
                movement_type="IN",
                quantity=purchase_item.quantity,
                reference_type="PURCHASE",
                reference_id=purchase.id,
                notes=f"Stock received from purchase #{purchase.id}"
            )

        # 5. Commit everything together
        db.commit()

        # 6. Refresh purchase
        db.refresh(purchase)

        return purchase

    except Exception:
        db.rollback()
        raise

def get_purchases(db: Session):
    return db.query(Purchase).order_by(Purchase.id.desc()).all()

def get_purchase_by_id(purchase_id: int, db: Session):
    purchase = (
        db.query(Purchase)
        .filter(Purchase.id == purchase_id)
        .first()
    )

    if not purchase:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )

    return purchase 