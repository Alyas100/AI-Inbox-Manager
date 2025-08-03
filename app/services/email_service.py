
from app.core.database import SessionLocal
from app.models.user import User
from app.services.gmail import fetch_gmail_messages
from app.services.oauth_refresh import refresh_access_token


def get_emails_for_user(email):
    db = SessionLocal()
    try:
        print("entering....")
        user = db.query(User).filter_by(email=email).first()
        # DEBUG
        print("Searching for: ", {email})

        print(user)
        if not user:
            raise Exception("User not found")
        try:
            return fetch_gmail_messages(user.access_token, user.refresh_token)

        except Exception as e:
            # if token expired or revoked, refresh it
            if "invalid_grant" in str(e).lower() or "expired" in str(e).lower():
                print("Access token expired, refreshing...")
                new_access_token = refresh_access_token(email)

                # Update the user's token in DB
                user.access_token = new_access_token
                db.commit()

                # retry fetching emails with the new token
                return fetch_gmail_messages(new_access_token, user.refresh_token)
            
            # if the error is something else, raise it
            raise

    finally:
        db.close()




       
