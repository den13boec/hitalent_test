from sqlalchemy.orm import Session
from app.models.answer import Answer


def get_answer(db: Session, aid: int):
    return db.query(Answer).filter(Answer.id == aid).first()


def create_answer(db: Session, question_id: int, user_id: str, text: str):
    a = Answer(question_id=question_id, user_id=user_id, text=text)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def delete_answer(db: Session, a: Answer):
    db.delete(a)
    db.commit()
