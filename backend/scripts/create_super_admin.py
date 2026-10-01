from sqlalchemy.orm import Session

from core.database import SessionLocal
from modules.auth.models import User
from core.security import hash_password


def create_super_admin():
    db: Session = SessionLocal()

    try:
        email = "superadmin@stockflow.com"

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("Super Admin already exists")
            return

        super_admin = User(
            name="Super Admin",
            email=email,
            password=hash_password("SuperAdmin@123"),
            role="super_admin"
        )

        db.add(super_admin)
        db.commit()

        print("Super Admin created successfully")

    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin()