from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Основная информация
    company = Column(String, nullable=False, index=True)
    position = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    
    # Рекрутер
    recruiter_name = Column(String, nullable=True)
    recruiter_contacts = Column(Text, nullable=True)
    screening_rating = Column(Integer, nullable=True)
    
    # Технический собеседующий
    interviewer_name = Column(String, nullable=True)
    tech_rating = Column(Integer, nullable=True)
    
    # Детали
    details = Column(Text, nullable=True)
    
    # Статус модерации
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="reviews")