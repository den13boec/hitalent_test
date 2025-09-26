from sqlalchemy.orm import Session
from app.models.question import Question


def list_questions(db: Session):
    return db.query(Question).order_by(Question.id).all()


def get_question(db: Session, qid: int):
    return db.query(Question).filter(Question.id == qid).first()


def create_question(db: Session, text: str):
    q = Question(text=text)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def delete_question(db: Session, q: Question):
    db.delete(q)
    db.commit()
