from fastapi import FastAPI
from app.api.routes import router as auth_router # LATER-create file inside app folder
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()

# add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


app.include_router(auth_router)

