from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Space(Base):
    __tablename__ = 'space'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1000), nullable=False)
    rent_price = Column(Float, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    bathrooms = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
