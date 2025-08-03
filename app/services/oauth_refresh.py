import os
import requests
from app.core.database import SessionLocal
from app.models.user import User

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def refresh_access_token(user_email):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=user_email).first()
        if not user or not user.refresh_token:
            raise Exception("No refresh token available for this user.")

        data = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": user.refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        token_data = response.json()

        if "access_token" not in token_data:
            raise Exception("Failed to refresh token: " + str(token_data))

        # Update user's access token in DB
        user.access_token = token_data["access_token"]
        db.commit()

        return token_data["access_token"]

    finally:
        db.close()
