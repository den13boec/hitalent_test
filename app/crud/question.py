from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.question import Question


def list_questions(db: Session) -> List[Question]:
    return db.query(Question).order_by(Question.id).all()


def get_question(db: Session, qid: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == qid).first()


def create_question(db: Session, text: str) -> Question:
    q = Question(text=text)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def delete_question(db: Session, q: Question) -> None:
    db.delete(q)
    db.commit()
