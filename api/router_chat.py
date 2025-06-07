from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from core.engine import Conversation

router = APIRouter(prefix="/chat")

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, rep: str):
    await ws.accept()
    convo = Conversation(rep)
    try:
        while True:
            msg = await ws.receive_text()
            reply = await convo.step(msg)
            await ws.send_text(reply)
    except WebSocketDisconnect:
        # Persist transcript + trigger grading
        ...

