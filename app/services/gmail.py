
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def fetch_gmail_messages(access_token, refresh_token=None):
    creds = Credentials(token=access_token)
    
    # Optional: implement token refresh here using refresh_token if needed

    service = build('gmail', 'v1', credentials=creds)
    
    # Get the latest 10 messages
    response = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = response.get('messages', [])

    return messages
