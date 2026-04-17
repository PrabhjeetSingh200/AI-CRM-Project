from sqlalchemy import Column, Integer, String, Text
from db import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    doctor = Column(String)
    company = Column(String)
    product = Column(String)
    notes = Column(Text)