from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "fuck u world"}
    
from sqlalchemy import create_engine,text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/test-db")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT now()"))
        return {"db_time": result.scalar()}
