from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.answer import AnswerOut
from app.crud import answer as acrud

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{aid}", response_model=AnswerOut)
def get_answer(aid: int, db: Session = Depends(get_db)) -> acrud.Answer:
    a = acrud.get_answer(db, aid)
    if not a:
        raise HTTPException(status_code=404, detail="Answer not found")
    return a


@router.delete("/{aid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(aid: int, db: Session = Depends(get_db)) -> None:
    a = acrud.get_answer(db, aid)
    if not a:
        raise HTTPException(status_code=404, detail="Answer not found")
    acrud.delete_answer(db, a)
    return
