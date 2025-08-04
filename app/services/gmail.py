
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64 # for ascii safe encoding
from bs4 import BeautifulSoup # parse html into a parse tree, then easily extract data
import re # regex
import html # to unescape HTML entities
import os
from dotenv import load_dotenv

load_dotenv()

def decode_bytes(data):
    for encoding in ['utf-8', 'windows-1252', 'iso-8859-1']:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode('utf-8', errors='ignore')  # Final fallback

# Parse HTML to clean plain text
def extract_plain_text_from_html(base64_html):
    html_bytes = base64.urlsafe_b64decode(base64_html).decode('utf-8', errors='ignore')
    html_raw = decode_bytes(html_bytes)


    # Unescape escaped characters like \u003C -> <
    html_raw = html_raw.encode().decode('unicode_escape')
    html_raw = html.unescape(html_raw)

    soup = BeautifulSoup(html_raw, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    return normalize_text(text)

# Normalize whitespace and remove excess characters
def normalize_text(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')  # Normalize newlines
    text = re.sub(r'\\[nrt]', '\n', text)  # Convert escaped \n, \r, \t to actual newlines
    text = re.sub(r'\n{2,}', '\n\n', text)  # Collapse multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Collapse multiple spaces/tabs
    text = text.strip()
    return text

def extract_body(payload):
    """
    Recursively extract the best plain text body from payload.
    """
    if 'parts' in payload:
        for part in payload['parts']:
            result = extract_body(part)
            if result:
                return result
    else:
        mime = payload.get("mimeType", "")
        data = payload.get("body", {}).get("data")
        if not data:
            return None

        try:
            if mime == "text/plain":
                raw = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                return normalize_text(raw)
            elif mime == "text/html":
                return extract_plain_text_from_html(data)
        except Exception as e:
            print(f"Decode error: {e}")
            return None
    return None

def fetch_gmail_messages(access_token, refresh_token=None):
    creds = Credentials(
        token=access_token,
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token"
        )
    
    # Optional: implement token refresh here using refresh_token if needed

    service = build('gmail', 'v1', credentials=creds)
    
    # Get the latest messages
    response = service.users().messages().list(userId='me', maxResults=3).execute()
    messages_ids = response.get('messages', [])

    messages = []

    

    for msg in messages_ids:
        msg_id = msg['id']
        msg_detail = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
        sender = next((h["value"] for h in headers if h["name"] == "From"), None)

        payload = msg_detail.get("payload", {})
        body = extract_body(payload)



        messages.append({
            "id": msg_id,
            "subject": subject,
            "from": sender,
            "body": body or ""
        })

    return messages
