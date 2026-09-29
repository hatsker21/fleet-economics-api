from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from src.config import settings

# Налаштовуємо хешування паролів алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    # Використовуємо timezone-aware UTC час
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
        
    to_encode.update({"exp": expire})
    
    # Створюємо JWT токен, підписаний нашим секретним ключем з .env
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt