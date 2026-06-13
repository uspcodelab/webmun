from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.session.schemas import SessionCreationSchema, SessionEvent
from .manager import manager
from .service import create_session, handle_client_messages


router = APIRouter()

#Workaround to make FastApi add all the Schemas to the OpenApi file
@router.get("/dummy", status_code=status.HTTP_404_NOT_FOUND)
async def dummy(name: SessionEvent):
    return Response(status_code=status.HTTP_404_NOT_FOUND)
    

# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_commitee(committeeInfo: SessionCreationSchema):
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
