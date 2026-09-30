from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.sales.models import Sale, SaleItem
from modules.sales.schema import SaleCreate
from modules.customers.models import Customer
from modules.products.models import Product
from modules.stock_movements.service import create_stock_movement


def create_sale(payload: SaleCreate, db: Session):
    # 1. Validate customer existence
    customer = (
        db.query(Customer)
        .filter(Customer.id == payload.customer_id)
        .first()
    )
    
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {payload.customer_id} not found."
        )
    
    # 2.Validate sale has items
    if not payload.items:
        raise HTTPException(
            status_code=400,
            detail="Sale must have at least one item."
        )
        
    total_amount = 0
    sale_items = []
    
    # 3. Validate all products and stock
    for item in payload.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {item.product_id} not found."
            )
            
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Insufficient stock for product "
                    f"'{product.name}'. "
                    f"Available: {product.quantity}, "
                    f"Requested: {item.quantity}"
                )
            )
        
        # 4. Calculate subtotal using current product price
        subtotal = item.quantity * product.price
        total_amount += subtotal
        
        sale_item = SaleItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        )
        sale_items.append(( sale_item, product))  # Store product for stock movement later
        
    # 5. Create sale record
    sale = Sale(
        customer_id=payload.customer_id,
        total_amount=total_amount,
        status="completed",
        items=[item[0] for item in sale_items]
    )
    
    try:
        db.add(sale)
        db.flush()  # Flush to get sale.id for stock movements
        
        # 6. Create sale items and update stock
        for sale_item, product in sale_items:
            sale_item.sale_id = sale.id
            
            db.add(sale_item)
            
            # Deduct stock
            product.quantity -= sale_item.quantity
            
            # 7. Create STOCK OUT movement
            create_stock_movement(
                db=db,
                product_id=product.id,
                movement_type="OUT",
                quantity=sale_item.quantity,
                reference_type="SALE",
                reference_id=sale.id,
                notes=f"Stock sold through sale #{sale.id}"
            )
        
        # 8. Commit transaction
        db.commit()
        db.refresh(sale)
        
        return sale

    except Exception:
        db.rollback()
        raise

def get_sales(db: Session):
    return (
        db.query(Sale)
        .order_by(Sale.id.desc())
        .all()
    )
    
def get_sale_by_id(sale_id: int, db: Session):
    sale = (
        db.query(Sale)
        .filter(Sale.id == sale_id)
        .first()
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale
