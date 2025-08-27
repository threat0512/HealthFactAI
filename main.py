from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import sqlite3

from database import get_db
from auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ✅ Register new user
@app.post("/register/")
def register(username: str, password: str):
    conn = get_db()
    c = conn.cursor()
    try:
        hashed_pw = get_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return {"msg": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

# ✅ Login → return JWT
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE username=?", (form_data.username,))
    user = c.fetchone()
    conn.close()

    if not user or not verify_password(form_data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[1]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Protected route
@app.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    from jose import jwt, JWTError
    from auth import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
