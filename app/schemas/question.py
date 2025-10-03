from __future__ import annotations
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict
from pydantic import StringConstraints, Field
from app.schemas.answer import AnswerOut

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class QuestionCreate(BaseModel):
    text: NonEmptyStr = Field(json_schema_extra={"example": "Your question"})


class QuestionOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class QuestionDetail(QuestionOut):
    answers: list[AnswerOut] = []
    model_config = ConfigDict(from_attributes=True)
