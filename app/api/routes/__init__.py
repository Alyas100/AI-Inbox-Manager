# app/api/routes/__init__.py
from .auth import router as auth_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router)
