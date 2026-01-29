from fastapi import FastAPI, Depends, HTTPException
from app.db import get_db, init_db
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.schemas import RegisterRequest, LoginRequest

app = FastAPI(title="Hackathon API")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "API running"}

# ---------- AUTH ----------

@app.post("/auth/register")
def register(data: RegisterRequest):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, hash_password(data.password)),
        )
        conn.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        cur.close()
        conn.close()

    return {"message": "User registered successfully"}

@app.post("/auth/login")
def login(data: LoginRequest):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=%s",
        (data.username,),
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row or not verify_password(data.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data.username)
    return {"access_token": token, "token_type": "bearer"}

# ---------- PROTECTED ----------

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": user["username"]
    }
