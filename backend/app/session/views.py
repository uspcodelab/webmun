# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.session.schemas import SessionCreationSchema, SessionEvent
from .manager import manager
from .service import create_session, handle_client_messages


router = APIRouter()

# Create session route
# TODO: improve session creation
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_session_endpoint(session_schema: SessionCreationSchema, test: SessionEvent): #terrible workaround to FastApi only adding schemas that are on routes to the openapi schemas
    # Mock a session being created
    create_session(session_schema)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, delegation: str):
    await manager.connect(websocket, session_id, delegation)
    try:
        while True:
            data = await websocket.receive_text()
            await handle_client_messages(
                    session_id=session_id,
                    sender=delegation, 
                    data=data,
            )
            # add broadcast state here if needed?

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

