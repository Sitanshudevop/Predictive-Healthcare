from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Mock authentication dependency.
    Always returns a Guest User (ID 1) to keep the DB history intact
    without requiring actual JWT verification.
    """
    # Check if guest user exists
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        # Create the guest user if it doesn't exist
        user = User(
            id=1,
            email="guest@predictivehealthcare.com",
            hashed_password="mock_hashed_password",
            full_name="Guest User",
            is_active=True,
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
