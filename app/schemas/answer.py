from pydantic import BaseModel, Field
from datetime import datetime

class AnswerCreate(BaseModel):
    user_id: str = Field(min_length=1, strip_whitespace=True)
    text: str = Field(min_length=1, strip_whitespace=True)

class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime
    class Config: from_attributes = True
