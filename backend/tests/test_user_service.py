import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a new user"""
    user_data = UserCreate(
        telegram_id=123456789,
        username="testuser",
        first_name="Test"
    )
    
    user = await UserService.create_user(db_session, user_data)
    
    assert user.id is not None
    assert user.telegram_id == 123456789
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.blocked is False

@pytest.mark.asyncio
async def test_get_user_by_telegram_id(db_session):
    """Test getting user by telegram_id"""
    # Create user
    user_data = UserCreate(telegram_id=987654321, username="another")
    created_user = await UserService.create_user(db_session, user_data)
    
    # Get user
    found_user = await UserService.get_user_by_telegram_id(db_session, 987654321)
    
    assert found_user is not None
    assert found_user.telegram_id == 987654321
    assert found_user.id == created_user.id

@pytest.mark.asyncio
async def test_get_or_create_user_creates_new(db_session):
    """Test get_or_create creates new user if not exists"""
    user = await UserService.get_or_create_user(
        db_session,
        telegram_id=111222333,
        username="newuser",
        first_name="New"
    )
    
    assert user.id is not None
    assert user.telegram_id == 111222333

@pytest.mark.asyncio
async def test_get_or_create_user_returns_existing(db_session):
    """Test get_or_create returns existing user"""
    # Create user first
    await UserService.get_or_create_user(db_session, telegram_id=555666777)
    
    # Try to get_or_create again
    user = await UserService.get_or_create_user(db_session, telegram_id=555666777)
    
    assert user.telegram_id == 555666777