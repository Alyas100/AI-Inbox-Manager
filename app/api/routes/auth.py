from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from app.services.oauth import oauth
from app.services.email_service import get_emails_for_user
from app.services.gemini import summarize_with_gemini
import sqlite3



router = APIRouter()


# function to retrieve user emailthat stored in db
def get_user_email(user_id: int = 2):
    conn = sqlite3.connect("test.db")  
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))  # Or use WHERE if multiple users
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else None


@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    # use access_type to get refresh token everytime, not just on first login
    # use prompt consent for login popup to appear everytime this endpoint is hit
    return await oauth.google.authorize_redirect(request, redirect_uri, access_type="offline", prompt="consent")


@router.get("/auth/google/callback", name="auth_callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print("RAW TOKEN DICT:", token)      # ← see what keys you have


    # Use userinfo directly from token response
    user_info = token.get('userinfo', {})
    
    # Debug print (remove in prod)s
    print("Logged in user:", user_info)
    
    return {"email": user_info["email"], "name": user_info["name"], "token": token}


# LATER: do function to use the refresh token to request again access token after the access token expired


#testing api func to fetch email 
@router.get("/test-fetch-emails")
def test_fetch_emails():
    email = get_user_email()
    messages = get_emails_for_user(email)
    return {"messages": messages}


@router.get("/summarize-emails")
def summarize_emails():
    email = get_user_email()
    messages = get_emails_for_user(email)

    # Format the emails into a string Gemini can summarize
    combined_messages = "\n\n".join(
        [f"From: {msg['from']}\nSubject: {msg['subject']}\nSnippet: {msg['body']}" for msg in messages]
    )

    prompt = (
        "Summarize the following email messages in **valid JSON** only. "
        "Your response must be a JSON object, not a string. "
        "Example:\n"
        "{\n"
        '  "summarization": {\n'
        '    "Sender A": [ "• point1", "• point2" ],\n'
        '    "Sender B": [ "• point1" ]\n'
        "  }\n"
        "}\n\n"
        "Now summarize:\n\n"
        + combined_messages
    )

    summary = summarize_with_gemini(prompt)
    return {"summarization": summary}



    