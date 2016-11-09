from sqlalchemy import Column, Integer, String, Enum, DateTime
from app import Base


class incomes_activities_earned_by(Base):
    __tablename__ = 'incomes_activities_earned_by'
    iid = Column(Integer, unique=True, nullable=False, primary_key=True)
    aid = Column(Integer, unique=True, nullable=False, primary_key=True)    
    sum = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    type = Column(String(50), nullable=False)
    #frequency = 
    sector = Column(String(50), nullable=False)
    FREQUENCY FREQ NOT NULL ,
    description = Column(String(200), nullable=False)
