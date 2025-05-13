# backend/app/ai.py
from dotenv import load_dotenv

# This will look in your current working directory (and parents) for “.env”
load_dotenv()

import os
from langchain import OpenAI, PromptTemplate, LLMChain
from .db import SessionLocal
from .models import Session as SessionModel

def summarize_session(session_id: int) -> str:
    # Fetch notes
    db = SessionLocal()
    sess = db.query(SessionModel).get(session_id)
    notes = sess.notes

    # Build prompt
    prompt = PromptTemplate(
        input_variables=["notes"],
        template="Summarize these study session notes succinctly:\n\n{notes}"
    )

    # Now the key is loaded into the environment
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError(
            "OPENAI_API_KEY not set—did you create backend/.env and run from the backend folder?"
        )

    llm = OpenAI(
        model_name="gpt-4o",
        openai_api_key=openai_key
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(notes=notes)
