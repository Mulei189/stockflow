from jose import jwt
from jose import JWTError

from fastapi import (Cookie, HTTPException, Depends)
from sqlalchemy.orm import Session
from core.database import get_db
from modules.auth.models import User

from core.security import(SECRET_KEY, ALGORITHM)

def get_current_user(db: Session = Depends(get_db), access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("id")

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )