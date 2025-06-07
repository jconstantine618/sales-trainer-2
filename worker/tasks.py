from celery import shared_task
from core.grading import grade_transcript
from db.session import async_sessionmaker
from db.crud import save_score

@shared_task
def async_score_transcript(conversation_id: str):
    import asyncio

    async def _runner():
        async with async_sessionmaker() as db:
            convo = await get_conversation_by_id(db, conversation_id)
            scored = await grade_transcript(convo.history)
            await save_score(db, conversation_id, scored)

    asyncio.run(_runner())
