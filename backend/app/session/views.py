# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.session.schemas import SessionCreationSchema, DelegateEvents, ChairEvents, SessionEvent
from .manager import manager, SessionLiveState 
from .service import create_session, handle_client_messages


router = APIRouter()

#Workaround to make FastApi add all the Schemas to the OpenApi file
@router.get("/dummy", status_code=status.HTTP_404_NOT_FOUND)
async def dummy(name: SessionEvent, schemas: SessionLiveState, enum1: DelegateEvents, enum2: ChairEvents):
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return Response(status_code=status.HTTP_200_OK)
    
# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_session_endpoint(session_schema: SessionCreationSchema): 
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

