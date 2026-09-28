from decimal import Decimal
from datetime import date

from pydantic import BaseModel


class AnalyticsOverviewResponse(BaseModel):
    total_products: int
    total_customers: int

    total_sales: int
    total_purchases: int

    total_units_sold: int
    total_units_purchased: int

    total_sales_revenue: Decimal
    total_purchase_cost: Decimal

    current_inventory_units: int
    current_inventory_value: Decimal
    
class SalesByDateResponse(BaseModel):
    date: date
    sales_count: int
    units_sold: int
    revenue: Decimal


class SalesAnalyticsResponse(BaseModel):
    total_sales: int
    total_units_sold: int
    total_revenue: Decimal
    average_sale_value: Decimal
    sales_by_date: list[SalesByDateResponse]
    
class ProductAnalyticsItemResponse(BaseModel):
    product_id: int
    product_name: str
    sku: str

    units_sold: int
    revenue: Decimal

    current_stock: int
    current_stock_value: Decimal


class ProductAnalyticsResponse(BaseModel):
    total_products: int
    products: list[ProductAnalyticsItemResponse]
    
class CustomerAnalyticsItemResponse(BaseModel):
    customer_id: int
    customer_name: str

    transaction_count: int
    units_purchased: int
    total_spent: Decimal
    average_transaction_value: Decimal


class CustomerAnalyticsResponse(BaseModel):
    total_customers: int
    customers: list[CustomerAnalyticsItemResponse]
    
class SupplierAnalyticsItemResponse(BaseModel):
    supplier_id: int
    supplier_name: str

    purchase_count: int
    units_purchased: int
    total_spent: Decimal
    average_purchase_value: Decimal


class PurchaseAnalyticsResponse(BaseModel):
    total_purchases: int
    total_units_purchased: int
    total_purchase_cost: Decimal
    average_purchase_value: Decimal

    suppliers: list[SupplierAnalyticsItemResponse]