from fastapi import FastAPI
from api.router_chat import router as chat_router
from api.router_score import router as score_router

app = FastAPI()
app.include_router(chat_router)
app.include_router(score_router)
