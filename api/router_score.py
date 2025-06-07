# api/router_score.py
"""
Routes that evaluate a rep’s performance against a rubric.

There are two entry points:

1. POST /score           – Client sends the full `history` list and receives
                           graded feedback immediately (synchronous).

2. POST /score/{id}      – Queues a Celery task that loads the transcript
                           for `conversation_id`, grades it, and stores the
                           result (asynchronous).  Returns a task‑ID so the
                           caller can poll if desired.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.grading import grade_transcript        # GPT rubric grader
from db.session import get_session               # async session factory
from db.crud import get_conversation_by_id       # fetch from Postgres
from worker.tasks import async_score_transcript  # Celery task

router = APIRouter(prefix="/score", tags=["score"])


# --------------------------------------------------------------------------- #
# 1️⃣  Synchronous grading – POST a transcript directly
# --------------------------------------------------------------------------- #
@router.post("/", summary="Grade a transcript (sync)")
async def score_history(payload: dict):
    """
    Request body:
    {
      "history": [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
        ...
      ]
    }
    """
    history = payload.get("history")
    if not history or not isinstance(history, list):
        raise HTTPException(
            status_code=400,
            detail="Request body must contain a 'history' list of messages.",
        )

    graded_json = await grade_transcript(history)   # calls OpenAI once
    return graded_json                              # already JSON‑serialisable


# --------------------------------------------------------------------------- #
# 2️⃣  Asynchronous grading – queue a job for a stored conversation
# --------------------------------------------------------------------------- #
@router.post("/{conversation_id}", summary="Grade stored conversation (async)")
async def score_by_id(
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
):
    """
    Looks up the transcript for `conversation_id`.  If found, pushes an
    async Celery job to grade it and persist the results.

    Response:
      {"status":"queued","task_id":"88b5c74e‑7e4d‑4c2a‑9f1b‑2c934e6b46e1"}
    """
    convo = await get_conversation_by_id(db, conversation_id)
    if convo is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    task_result = async_score_transcript.delay(conversation_id)
    return {"status": "queued", "task_id": str(task_result.id)}

