from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from .models import Category

# create category
def create_category(db: Session, payload):
    data = payload.model_dump()

    # check for existing category
    existing_category = (
        db.query(Category)
        .filter(Category.name == data["name"])
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    
    # create new category
    new_category = Category(**data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "success": True,
        "message": "Category created successfully",
        "new_category": new_category
    }

# get all categories
def get_categories(db: Session):
    categories = db.query(Category).all()

    return {
        "success": True,
        "message": "Categories retrieved successfully",
        "count": len(categories),
        "categories": categories
    }

# get category by id
def get_category(category_id: int, db: Session):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

# check if category exists
    if not category:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return {
        "success": True,
        "message": "Category retrieved successfully",
        "category": category
    }


# update category
def update_category(db: Session, category_id: int, payload):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    data = payload.model_dump(exclude_unset=True)

    if "name" in data:
        existing = (
            db.query(Category)
            .filter(Category.name == data["name"])
            .first()
        )

        if existing and existing.id != category.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )

    for key, value in data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return {
        "success": True,
        "message": "Category updated successfully",
        "category": category
    }


# delete category
def delete_category(db: Session, category_id: int):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "success": True,
        "message": "Category deleted successfully"
    }
