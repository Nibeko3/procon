from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta,timezone
import models, schemas
from database import get_db
import os


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# パスワードハッシュ
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 登録
@router.post("/register")
def register(user: schemas.PlayerCreate, db: Session = Depends(get_db)):
    if db.query(models.Player).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = models.Player(
        username=user.username,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# ログイン
@router.post("/login")
def login(user: schemas.PlayerLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.Player).filter_by(username=user.username).first()

    if db_user is None or db_user.password_hash is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        access_token = create_access_token(data={"sub": db_user.username})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token error: {str(e)}")

    return {"access_token": access_token, "token_type": "bearer"}

'''@router.post("/login")
def login(user: schemas.PlayerLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.Player).filter_by(username=user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}'''
