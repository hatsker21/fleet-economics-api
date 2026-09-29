from pydantic import BaseModel, EmailStr
from src.models.user import UserRole

# Схема того, що юзер відправляє при реєстрації
class UserRegisterRequest(BaseModel):
    company_name: str
    email: EmailStr
    password: str

# Схема того, що ми віддаємо назад (без пароля!)
class UserResponse(BaseModel):
    id: int
    company_id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True  # Дозволяє Pydantic читати дані з SQLAlchemy моделей

# Схема для токена авторизації
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"