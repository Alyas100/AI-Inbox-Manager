


from app.core.database import SessionLocal
from app.models.user import User

def save_or_update_user(email, access_token, refresh_token):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if user:
            user.access_token = access_token
            user.refresh_token = refresh_token or user.refresh_token
        else:
            user = User(
                email=email,
                access_token=access_token,
                refresh_token=refresh_token
            )
            db.add(user)
        db.commit()
        db.refresh(user)  # load everything now
        return {
            "id": user.id,
            "email": user.email,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token
        }
    finally:
        db.close()

