from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
        result = await db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str = None, first_name: str = None) -> User:
        user = await UserService.get_user_by_telegram_id(db, telegram_id)
        if not user:
            user_data = UserCreate(telegram_id=telegram_id, username=username, first_name=first_name)
            user = await UserService.create_user(db, user_data)
        return user