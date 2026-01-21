from fastapi import FastAPI

from app.database import engine
from app import models
from app.auth.routes import router as auth_router
from app.chat.routes import router as chat_router

app = FastAPI(title="AI Chat Assistant API")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
