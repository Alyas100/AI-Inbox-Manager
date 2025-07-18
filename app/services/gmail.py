
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def fetch_gmail_messages(access_token, refresh_token=None):
    creds = Credentials(
        token=access_token,
        client_id="555750767356-olt7uoudaj1v4jfs42a8i6p8r9m1m0r9.apps.googleusercontent.com",
        client_secret="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",
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token"
        )
    
    # Optional: implement token refresh here using refresh_token if needed

    service = build('gmail', 'v1', credentials=creds)
    
    # Get the latest 10 messages
    response = service.users().messages().list(userId='me', maxResults=5).execute()
    messages_ids = response.get('messages', [])

    messages = []

    for msg in messages_ids:
        msg_id = msg['id']
        msg_detail = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
        sender = next((h["value"] for h in headers if h["name"] == "From"), None)
        snippet = msg_detail.get("snippet", "")

        messages.append({
            "id": msg_id,
            "subject": subject,
            "from": sender,
            "snippet": snippet
        })

    return messages
