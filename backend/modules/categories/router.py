from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from .schemas import CreateCategory, UpdateCategory
from .service import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.post("/")
def create_category_endpoint(
    payload: CreateCategory,
    db: Session = Depends(get_db)
):
    return create_category(db, payload)


@router.get("/")
def get_categories_endpoint(
    db: Session = Depends(get_db)
):
    return get_categories(db)


@router.get("/{category_id}")
def get_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
):
    return get_category(category_id, db)


@router.put("/{category_id}")
def update_category_endpoint(
    category_id: int,
    payload: UpdateCategory,
    db: Session = Depends(get_db)
):
    return update_category(db, category_id, payload)


@router.delete("/{category_id}")
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
):
    return delete_category(
        db,
        category_id
    )


