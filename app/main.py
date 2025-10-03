from fastapi import FastAPI
from app.api.routers.questions import router as questions_router
from app.api.routers.answers import router as answers_router
from app.api.routers.questions import nested_answers_router


app = FastAPI(title="QnA API")

# /questions (list/create/get/delete)
app.include_router(questions_router)

# POST /questions/{qid}/answers/ (will go to "answers")
app.include_router(nested_answers_router)

# /answers/{aid} get/delete
app.include_router(answers_router)
