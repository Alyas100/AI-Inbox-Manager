from app.core.database import SessionLocal
from app.models.email import EmailMessage
from app.models.user import User

def save_fetched_emails_to_db(user_email, messages):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=user_email).first()
        if not user:
            raise Exception("User not found")

        for msg in messages:
            # Check if email already exists (avoid duplicates)
            exists = db.query(EmailMessage).filter_by(
                user_id=user.id, subject=msg["subject"], sender=msg["from"]
            ).first()
            if exists:
                continue

            new_email = EmailMessage(
                user_id=user.id,
                sender=msg["from"],
                subject=msg["subject"],
                body=msg["body"]
            )
            db.add(new_email)

        db.commit()
    finally:
        db.close()
