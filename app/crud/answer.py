from typing import Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.answer import Answer


def get_answer(db: Session, aid: int) -> Optional[Answer]:
    return db.query(Answer).filter(Answer.id == aid).first()


def create_answer(
    db: Session, question_id: int, user_id: Optional[str], text: str
) -> Answer:
    uid = (user_id or "").strip() or str(uuid4())
    t = text.strip()
    a = Answer(question_id=question_id, user_id=uid, text=t)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def delete_answer(db: Session, a: Answer):
    db.delete(a)
    db.commit()
