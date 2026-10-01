from sqlalchemy.orm import Session
from core.database import SessionLocal
from modules.auth.models import User
from core.security import hash_password

def create_admin():
    db: Session = SessionLocal()

    try:
        email = "admin@stockflow.com"

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("Admin already exists")
            return

        admin = User(
            name="System Admin",
            email=email,
            password=hash_password("Admin@123"),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Admin created successfully")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
