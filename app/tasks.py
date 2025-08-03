from app.services.email_service import get_emails_for_user
from celery_app import celery
from app.core.database import SessionLocal
from app.models.email import EmailMessage

@celery.task(name="app.tasks.fetch_and_store_emails")
def fetch_and_store_emails(user_email):
    db = SessionLocal()
    try:
        print("DEBUG: Fetching emails for:", user_email)
        messages = get_emails_for_user(user_email) 
        print("DEBUG: Message fetched:", messages)
 

        for msg in messages:
            print("📌 DEBUG: Processing message:", msg)

            new_email = EmailMessage(
                user_id=None,
                sender=msg.get('from'),
                subject=msg.get('subject'),
                body=msg.get('body')
            )
            db.add(new_email)

        db.commit()
        print("✅ DEBUG: Successfully saved all emails")

        return f"Fetched and stored {len(messages)} emails for {user_email}"

    except Exception as e:
        print("❌ DEBUG: Error occurred:", str(e))

        return f"Error fetching emails: {str(e)}"
    finally:
        db.close()
