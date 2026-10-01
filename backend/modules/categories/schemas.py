from typing import Optional
from pydantic import BaseModel

class CreateCategory(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateCategory(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True
        