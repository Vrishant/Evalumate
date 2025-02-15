from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    chatroom_No: int
    file_name: str
    file_type: str


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    vector_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
