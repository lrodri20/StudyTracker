from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from celery import Celery
from .db import SessionLocal, init_db
from .models import Session as SessionModel
from .ai import summarize_session
from fastapi.middleware.cors import CORSMiddleware

# on startup, ensure tables exist
init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    celery_summary.delay(sess.id)
    return {"id": sess.id}
@app.get("/sessions/")
def get_all_sessions():
    db = SessionLocal()
    sessions = db.query(SessionModel).all()
    # Optionally, convert ORM models to dicts:
    return [
        {
            "id": s.id,
            "topic": s.topic,
            "duration_minutes": s.duration_minutes,
            "notes": s.notes,
            "summary": s.summary,
        }
        for s in sessions
    ]
@celery.task
def celery_summary(session_id: int):
    summary = summarize_session(session_id)
    db = SessionLocal()
    sess = db.query(SessionModel).get(session_id)
    sess.summary = summary
    db.commit()
