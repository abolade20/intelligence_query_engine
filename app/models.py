from sqlalchemy import Column, String, Integer, Float, DateTime
from uuid6 import uuid7
from datetime import datetime
from .database import Base

def generate_uuid():
    return str(uuid7())

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)

    gender = Column(String)
    gender_probability = Column(Float)

    age = Column(Integer)
    age_group = Column(String)

    country_id = Column(String(2))
    country_name = Column(String)
    country_probability = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)