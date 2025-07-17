# check_user.py
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter_by(email="alyasmuhd1234@gmail.com").first()
if user:
    print("✅ Found user:", user.email)
else:
    print("❌ User not found")
