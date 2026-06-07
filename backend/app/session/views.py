# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.session.schemas import SessionCreationSchema, SessionEvent
from .manager import manager
from .service import create_session, handle_client_messages


router = APIRouter()

# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_commitee(committeeInfo: SessionCreationSchema, test: SessionEvent):#terrible workaround to FastApi only adding schemas that are on routes to the openapi schemas
    # Mock a committee being created
    create_session(committeeInfo.committee_id, committeeInfo.name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.websocket("/ws/{committee_id}")
async def websocket_endpoint(websocket: WebSocket, committee_id: int):
    await manager.connect(websocket, committee_id)
    try:
        while True:
            data = await websocket.receive_text()
            handle_client_messages(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, committee_id)
