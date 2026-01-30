from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Создаем async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Логирование SQL запросов (отключить в продакшене)
    future=True
)

# Session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base для моделей
Base = declarative_base()

# Dependency для получения сессии
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session