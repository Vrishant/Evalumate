import string
from .database import Base
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from datetime import datetime


class Nex_doc(Base):
    __tablename__ = "nex_doc"
    id = Column(Integer, primary_key=True, index=True)
    chatroom_No = Column(Integer)
    file_name = Column(String, nullable=False)
    vector_id = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
