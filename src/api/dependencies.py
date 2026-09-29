from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.database import get_db
from src.config import settings
from src.models.user import User, UserRole

# Цей рядок каже Swagger UI, куди відправляти логін/пароль при натисканні кнопки "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Розшифровуємо JWT токен використовуючи наш секретний ключ
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Шукаємо користувача в БД
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    # Реалізація Soft Delete перевірки
    if user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Користувач деактивований"
        )
        
    return user

# Фабрика залежностей для перевірки ролей (RBAC)
def require_roles(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостатньо прав для виконання цієї дії"
            )
        return current_user
    return role_checker