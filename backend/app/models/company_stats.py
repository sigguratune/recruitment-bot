from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class CompanyStats(Base):
    __tablename__ = "companies_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, nullable=False, index=True)
    
    # Статистика
    reviews_count = Column(Integer, default=0)
    avg_screening_rating = Column(Float, nullable=True)
    avg_tech_rating = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())