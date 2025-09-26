from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class QuestionCreate(BaseModel):
    text: str = Field(min_length=1, strip_whitespace=True)


class QuestionOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerOut(BaseModel):
    id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionDetail(QuestionOut):
    answers: List[AnswerOut] = []
