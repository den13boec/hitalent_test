from __future__ import annotations
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, StringConstraints, Field

# convenient aliases
StrippedStr = Annotated[str, StringConstraints(strip_whitespace=True)]
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class AnswerCreate(BaseModel):
    user_id: Optional[StrippedStr] = Field(
        default=None, json_schema_extra={"example": ""}
    )
    text: NonEmptyStr = Field(json_schema_extra={"example": "Your answer"})


class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
