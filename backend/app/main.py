from fastapi import FastAPI
from app.db import get_db

app = FastAPI(title="Hackathon API")

@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/health")
def health():
    return {"health": "ok"}

@app.get("/db-check")
def db_check():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    return {"db": "connected"}
