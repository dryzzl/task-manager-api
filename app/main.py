from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0"
)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Task Manager API Running"}