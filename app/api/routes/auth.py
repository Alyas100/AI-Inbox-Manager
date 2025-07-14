from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from app.services.oauth import oauth

router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback", name="auth_callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print("RAW TOKEN DICT:", token)      # ← see what keys you have


    # Use userinfo directly from token response
    user_info = token.get('userinfo', {})
    
    # Debug print (remove in prod)s
    print("Logged in user:", user_info)
    
    return {"email": user_info["email"], "name": user_info["name"], "token": token}

