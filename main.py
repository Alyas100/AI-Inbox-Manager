from fastapi import FastAPI
from app.api.routes import router as auth_router # LATER-create file inside app folder
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import Base, engine
from app.models import user 

app = FastAPI()

# add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


app.include_router(auth_router)

# LATER: suggestion to organize later
# app.include_router(
#     auth_router,
#     prefix="/api/v1",        # ← All routes get this prefix
#     tags=["authentication"]   # ← For OpenAPI docs grouping
# )


# Creates tables in the database
Base.metadata.create_all(bind=engine)
