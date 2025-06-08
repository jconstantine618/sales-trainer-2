from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Conversation, ConversationScore

async def get_conversation_by_id(db: AsyncSession, convo_id: str):
    res = await db.execute(select(Conversation).where(Conversation.id == convo_id))
    return res.scalar_one_or_none()

async def save_conversation(db: AsyncSession, rep_name: str, history: list[dict]):
    convo = Conversation(rep_name=rep_name, history=history)
    db.add(convo)
    await db.commit()
    await db.refresh(convo)
    return convo

async def save_score(db: AsyncSession, convo_id: str, graded: dict):
    convo = await get_conversation_by_id(db, convo_id)
    if convo is None:
        raise ValueError("Conversation not found")

    if convo.score:
        convo.score.scores = graded["scores"]
        convo.score.feedback = graded["feedback"]
    else:
        convo.score = ConversationScore(conversation_id=convo_id,
                                        scores=graded["scores"],
                                        feedback=graded["feedback"])
    await db.commit()
