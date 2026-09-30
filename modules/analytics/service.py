from sqlalchemy.orm import Session
from sqlalchemy import func

from modules.products.models import Product
from modules.customers.models import Customer
from modules.sales.models import Sale, SaleItem
from modules.purchases.model import Purchase, PurchaseItem
from modules.customers.models import Customer
from modules.suppliers.models import Supplier

# Analytics Overview
def get_analytics_overview(db: Session):
    # Total products
    total_products = (
        db.query(func.count(Product.id))
        .scalar()
        or 0
    )
    
# Total customers
    total_customers = (
        db.query(func.count(Customer.id))
        .scalar()
        or 0
    )

    # Total sales
    total_sales = (
        db.query(func.count(Sale.id))
        .scalar()
        or 0
    )

    # Total purchases
    total_purchases = (
        db.query(func.count(Purchase.id))
        .scalar()
        or 0
    )

    # Total units sold
    total_units_sold = (
        db.query(func.coalesce(func.sum(SaleItem.quantity), 0))
        .scalar()
        or 0
    )

    # Total units purchased
    total_units_purchased = (
        db.query(func.coalesce(func.sum(PurchaseItem.quantity), 0))
        .scalar()
        or 0
    )

    # Total sales revenue
    total_sales_revenue = (
        db.query(
            func.coalesce(func.sum(Sale.total_amount), 0)
        )
        .scalar()
        or 0
    )

    # Total purchase cost
    total_purchase_cost = (
        db.query(
            func.coalesce(func.sum(Purchase.total_amount), 0)
        )
        .scalar()
        or 0
    )

    # Current inventory units
    current_inventory_units = (
        db.query(
            func.coalesce(func.sum(Product.quantity), 0)
        )
        .scalar()
        or 0
    )

    # Current inventory value
    current_inventory_value = (
        db.query(
            func.coalesce(
                func.sum(Product.quantity * Product.price),
                0
            )
        )
        .scalar()
        or 0
    )

    return {
        "total_products": total_products,
        "total_customers": total_customers,

        "total_sales": total_sales,
        "total_purchases": total_purchases,

        "total_units_sold": total_units_sold,
        "total_units_purchased": total_units_purchased,

        "total_sales_revenue": total_sales_revenue,
        "total_purchase_cost": total_purchase_cost,

        "current_inventory_units": current_inventory_units,
        "current_inventory_value": current_inventory_value,
    }
    
# Sales Analytics
def get_sales_analytics(db: Session):
    total_sales = (
        db.query(func.count(Sale.id)).scalar() or 0
    )

    total_units_sold = (
        db.query(
            func.coalesce(func.sum(SaleItem.quantity), 0)
        ).scalar() or 0
    )

    total_revenue = (
        db.query(
            func.coalesce(func.sum(Sale.total_amount), 0)
        ).scalar() or 0
    )

    average_sale_value = (
        total_revenue / total_sales
        if total_sales > 0
        else 0
    )

    sales_by_date = (
        db.query(
            func.date(Sale.sale_date).label("date"),
            func.count(Sale.id).label("sales_count"),
            func.coalesce(func.sum(SaleItem.quantity), 0).label("units_sold"),
            func.coalesce(func.sum(SaleItem.subtotal), 0).label("revenue"),
        )
        .join(SaleItem, Sale.id == SaleItem.sale_id)
        .group_by(func.date(Sale.sale_date))
        .order_by(func.date(Sale.sale_date).desc())
        .all()
    )

    return {
        "total_sales": total_sales,
        "total_units_sold": total_units_sold,
        "total_revenue": total_revenue,
        "average_sale_value": average_sale_value,
        "sales_by_date": [
            {
                "date": row.date,
                "sales_count": row.sales_count,
                "units_sold": row.units_sold,
                "revenue": row.revenue,
            }
            for row in sales_by_date
        ],
    }
    

def get_product_analytics(db: Session):
    products = (
        db.query(Product)
        .order_by(Product.id.asc())
        .all()
    )

    product_sales = (
        db.query(
            SaleItem.product_id,
            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            ).label("units_sold"),
            func.coalesce(
                func.sum(SaleItem.subtotal),
                0
            ).label("revenue"),
        )
        .group_by(SaleItem.product_id)
        .all()
    )

    sales_lookup = {
        row.product_id: row
        for row in product_sales
    }

    product_analytics = []

    for product in products:
        sales = sales_lookup.get(product.id)

        units_sold = sales.units_sold if sales else 0
        revenue = sales.revenue if sales else 0

        product_analytics.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "units_sold": units_sold,
                "revenue": revenue,
                "current_stock": product.quantity,
                "current_stock_value": (
                    product.quantity * product.price
                ),
            }
        )

    return {
        "total_products": len(products),
        "products": product_analytics,
    }
    
def get_customer_analytics(db: Session):
    customers = (
        db.query(Customer)
        .order_by(Customer.id.asc())
        .all()
    )

    customer_sales = (
        db.query(
            Sale.customer_id,
            func.count(Sale.id).label("transaction_count"),
            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            ).label("units_purchased"),
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            ).label("total_spent"),
        )
        .join(
            SaleItem,
            Sale.id == SaleItem.sale_id
        )
        .group_by(Sale.customer_id)
        .all()
    )

    customer_lookup = {
        row.customer_id: row
        for row in customer_sales
    }

    customer_analytics = []

    for customer in customers:
        sales = customer_lookup.get(customer.id)

        transaction_count = (
            sales.transaction_count
            if sales
            else 0
        )

        units_purchased = (
            sales.units_purchased
            if sales
            else 0
        )

        total_spent = (
            sales.total_spent
            if sales
            else 0
        )

        average_transaction_value = (
            total_spent / transaction_count
            if transaction_count > 0
            else 0
        )

        customer_analytics.append(
            {
                "customer_id": customer.id,
                "customer_name": customer.name,
                "transaction_count": transaction_count,
                "units_purchased": units_purchased,
                "total_spent": total_spent,
                "average_transaction_value": (
                    average_transaction_value
                ),
            }
        )

    return {
        "total_customers": len(customers),
        "customers": customer_analytics,
    }

def get_purchase_analytics(db: Session):
    total_purchases = (
        db.query(func.count(Purchase.id)).scalar() or 0
    )

    total_units_purchased = (
        db.query(
            func.coalesce(func.sum(PurchaseItem.quantity), 0)
        ).scalar() or 0
    )

    total_purchase_cost = (
        db.query(
            func.coalesce(func.sum(Purchase.total_amount), 0)
        ).scalar() or 0
    )

    average_purchase_value = (
        total_purchase_cost / total_purchases
        if total_purchases > 0
        else 0
    )

    suppliers = (
        db.query(Supplier)
        .order_by(Supplier.id.asc())
        .all()
    )

    supplier_analytics = []

    for supplier in suppliers:
        purchase_count = (
            db.query(func.count(Purchase.id))
            .filter(Purchase.supplier_id == supplier.id)
            .scalar()
            or 0
        )

        units_purchased = (
            db.query(
                func.coalesce(func.sum(PurchaseItem.quantity), 0)
            )
            .join(
                Purchase,
                Purchase.id == PurchaseItem.purchase_id
            )
            .filter(Purchase.supplier_id == supplier.id)
            .scalar()
            or 0
        )

        total_spent = (
            db.query(
                func.coalesce(func.sum(Purchase.total_amount), 0)
            )
            .filter(Purchase.supplier_id == supplier.id)
            .scalar()
            or 0
        )

        average_supplier_purchase = (
            total_spent / purchase_count
            if purchase_count > 0
            else 0
        )

        supplier_analytics.append(
            {
                "supplier_id": supplier.id,
                "supplier_name": supplier.name,
                "purchase_count": purchase_count,
                "units_purchased": units_purchased,
                "total_spent": total_spent,
                "average_purchase_value": average_supplier_purchase,
            }
        )

    return {
        "total_purchases": total_purchases,
        "total_units_purchased": total_units_purchased,
        "total_purchase_cost": total_purchase_cost,
        "average_purchase_value": average_purchase_value,
        "suppliers": supplier_analytics,
    }

def get_dashboard_analytics(db: Session):
    return {
        "overview": get_analytics_overview(db),
        "sales": get_sales_analytics(db),
        "products": get_product_analytics(db),
        "customers": get_customer_analytics(db),
        "purchases": get_purchase_analytics(db),
    }