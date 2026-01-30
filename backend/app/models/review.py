from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

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
    recruiter_contacts = Column(Text, nullable=True)  # JSON строка
    screening_rating = Column(Integer, nullable=True)  # 1-10
    
    # Технический собеседующий
    interviewer_name = Column(String, nullable=True)
    tech_rating = Column(Integer, nullable=True)  # 1-10
    
    # Детали
    details = Column(Text, nullable=True)
    
    # Статус модерации
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="reviews")