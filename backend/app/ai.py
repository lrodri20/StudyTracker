from langchain import OpenAI, PromptTemplate, LLMChain
from .db import SessionLocal
from .models import Session as SessionModel
def summarize_session(session_id: int) -> str:
    # 1) Fetch stored notes from the DB
    db = SessionLocal()
    sess = db.query(SessionModel).get(session_id)
    notes = sess.notes

    # 2) Build a simple LangChain prompt
    prompt = PromptTemplate(
        input_variables=["notes"],
        template="Summarize these study session notes succinctly:\n\n{notes}"
    )
    llm = OpenAI(model_name="gpt-4o")
    chain = LLMChain(llm=llm, prompt=prompt)

    # 3) Run and return the summary
    summary = chain.run(notes=notes)
    return summary
