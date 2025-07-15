# test_db.py

from app.core.database import SessionLocal, Base, engine
from app.models.user import User

# Create the tables (only needed if not already done)
Base.metadata.create_all(bind=engine)

# Get DB session
db = SessionLocal()

# Create a new user instance
new_user = User(
    email="testuser@example.com",
    access_token="fake_access_token_123",
    refresh_token="fake_refresh_token_123"
)

# Add and commit to DB
db.add(new_user)
db.commit()
db.refresh(new_user)  # refresh to get ID and updated fields

# Query the user back
retrieved_user = db.query(User).filter_by(email="testuser@example.com").first()

print("User added and retrieved from DB:")
print(f"ID: {retrieved_user.id}, Email: {retrieved_user.email}")

db.close()
