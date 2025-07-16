
from app.core.database import SessionLocal
from app.models.user import User
from app.services.gmail import fetch_gmail_messages

def get_emails_for_user(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise Exception("User not found")

        access_token = user.access_token
        refresh_token = user.refresh_token

        return fetch_gmail_messages(access_token, refresh_token)
    finally:
        db.close()
