from pydantic import BaseModel
from pydantic import EmailStr

class SignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
    class Config:
        from_attributes = True