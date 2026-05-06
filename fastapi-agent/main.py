import logging
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import after env vars are loaded
from agent import get_agent, run_agent


# ── Startup: warm up the singleton agent ───────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting — initialising singleton agent…")
    get_agent()   # creates & caches the agent
    logger.info("Agent ready. Accepting requests.")
    yield
    logger.info("Server shutting down.")


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title="LangChain RAG Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas ────────────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(body: QuestionRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    try:
        answer = run_agent(body.question)
        return AnswerResponse(question=body.question, answer=answer)
    except Exception as exc:
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail=str(exc))


# ── Run locally ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
