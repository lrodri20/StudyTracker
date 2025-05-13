from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from celery import Celery
from .db import SessionLocal, init_db
from .models import Session as SessionModel
from .ai import summarize_session

# on startup, ensure tables exist
init_db()

app = FastAPI()
celery = Celery(broker="redis://localhost:6379/0")

# Pydantic schema for request validation
class SessionIn(BaseModel):
    topic: str
    duration_minutes: int
    notes: str

@app.post("/sessions/")
def create_session(
    payload: SessionIn,
    background_tasks: BackgroundTasks
):
    db = SessionLocal()
    # persist
    sess = SessionModel(**payload.dict())
    db.add(sess)
    db.commit()
    db.refresh(sess)

    # schedule summary generation
    background_tasks.add_task(celery_summary.delay, sess.id)
    return {"id": sess.id}

@celery.task
def celery_summary(session_id: int):
    summary = summarize_session(session_id)
    db = SessionLocal()
    sess = db.query(SessionModel).get(session_id)
    sess.summary = summary
    db.commit()
