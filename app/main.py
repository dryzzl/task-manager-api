from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Task Manager API Running"}

Base.metadata.create_all(bind=engine)