from pydantic import BaseModel

class CreateSupplierSchema(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    
class UpdateSupplierSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    
class SupplierResponse(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True