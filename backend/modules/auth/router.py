from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from modules.auth.schemas import SignUpSchema, LoginSchema, UserResponse
from modules.auth.services import create_user, login_user
from core.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import User

router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication']
)

@router.post('/signup')
def signup(
    payload: SignUpSchema,
    db: Session = Depends(get_db)
):

    user = create_user(payload, db)
    return {
        "success": True,
        "message": "User created successfully",
        "user": user
    }

@router.post('/login')
def login(payload: LoginSchema, response: Response, db: Session = Depends(get_db)):
    result = login_user(
        payload.email,
        payload.password,
        db
    )

    response.set_cookie(
        key="access_token",
        value=result["token"],
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return {
        "success": True,
        "message": "User logged in successfully",
        "user": UserResponse.model_validate(result["user"])
    }

@router.get('/me', response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return {
        "success": True,
        "message": "User logged out successfully"
    }