from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.question import QuestionCreate, QuestionOut, QuestionDetail
from app.crud import question as qcrud
from app.crud import answer as acrud
from app.schemas.answer import AnswerOut, AnswerCreate

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    return qcrud.list_questions(db)


@router.post("/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    return qcrud.create_question(db, text=payload.text)


@router.get("/{qid}", response_model=QuestionDetail)
def get_question(qid: int, db: Session = Depends(get_db)):
    q = qcrud.get_question(db, qid)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    # answers will be pulled up through Relationship, Pydantic will collect them
    return q


@router.delete("/{qid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(qid: int, db: Session = Depends(get_db)):
    q = qcrud.get_question(db, qid)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    qcrud.delete_question(db, q)
    return


@router.post(
    "/{qid}/answers/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED
)
def create_answer_for_question(
    qid: int, payload: AnswerCreate, db: Session = Depends(get_db)
):
    q = qcrud.get_question(db, qid)
    if not q:
        raise HTTPException(status_code=400, detail="Question does not exist")
    return acrud.create_answer(
        db, question_id=qid, user_id=payload.user_id, text=payload.text
    )
