from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from .service import create_product, get_products, get_product, update_product, delete_product
from .schemas import CreateProductSchema, UpdateProductSchema, ProductResponse

router = APIRouter(
    prefix='/api/products',
    tags=['Products']
)

@router.post("/")
def create_product_endpoint(payload: CreateProductSchema, db: Session = Depends(get_db)):
    return create_product(payload, db)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}")
def get_one(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)

@router.patch("/{product_id}")
def update(product_id: int, payload: UpdateProductSchema, db: Session = Depends(get_db)):
    return update_product(db, product_id, payload)

@router.delete("/{product_id}")
def remove(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)