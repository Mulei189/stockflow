from fastapi import FastAPI
from core.database import Base, engine
from modules.auth.router import router as auth_router
from modules.products.router import router as products_router
from modules.categories.router import router as categories_router
from modules.suppliers.router import router as suppliers_router
from modules.customers.router import router as customers_router
from modules.purchases.router import router as purchases_router
from modules.stock_movements.router import (
    router as stock_movements_router
)
from modules.sales.router import router as sales_router
from modules.inventory.router import router as inventory_router
from modules.analytics.router import router as analytics_router
from core.exceptions import global_exception_handler

app = FastAPI(
    title="StockFlow API",
    description="API for inventory and sales management",
    version="1.0.0"
)

# Add the global exception handler
app.add_exception_handler(
    Exception, global_exception_handler
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(suppliers_router)
app.include_router(customers_router)
app.include_router(purchases_router)
app.include_router(stock_movements_router)
app.include_router(sales_router)
app.include_router(inventory_router)
app.include_router(analytics_router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "StockFlow API Running"
    }

# Health check endpoint
@app.get('/health')
def health():
    return {
        "status": "healthy!"
    }