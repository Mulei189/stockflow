from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from modules.analytics.schema import (
    AnalyticsOverviewResponse,
    SalesAnalyticsResponse,
    ProductAnalyticsResponse,
    CustomerAnalyticsResponse,
    PurchaseAnalyticsResponse,
)
from modules.analytics.service import (
    get_analytics_overview,
    get_sales_analytics,
    get_product_analytics,
    get_customer_analytics,
    get_purchase_analytics,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/overview", response_model=AnalyticsOverviewResponse)
def get_overview(
    db: Session = Depends(get_db)
):
    return get_analytics_overview(db)


@router.get("/sales", response_model=SalesAnalyticsResponse)
def get_sales_analytics_data(db: Session = Depends(get_db)):
    return get_sales_analytics(db)

@router.get("/products", response_model=ProductAnalyticsResponse)
def get_product_analytics_data(db: Session = Depends(get_db)):
    return get_product_analytics(db)

@router.get("/customers", response_model=CustomerAnalyticsResponse)
def get_customer_analytics_data(db: Session = Depends(get_db)):
    return get_customer_analytics(db)

@router.get("/purchases", response_model=PurchaseAnalyticsResponse)
def get_purchase_analytics_data(db: Session = Depends(get_db)):
    return get_purchase_analytics(db)