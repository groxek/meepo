from fastapi import APIRouter, HTTPException, status
import bcrypt
from sqlalchemy import select

from database import AsyncSessionLocal
from models import User
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.username == user_data.username)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )

        hashed_pwd = hash_password(user_data.password)

        new_user = User(
            username=user_data.username,
            hashed_password=hashed_pwd
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user