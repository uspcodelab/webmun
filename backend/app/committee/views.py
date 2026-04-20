from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.committee.schemas import CommitteeStateSchema, CommitteeCreationSchema
from .manager import manager
from .service import create_committee

router = APIRouter()

# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_commitee(committeeInfo: CommitteeCreationSchema):
    # Mock a committee being created
    create_committee(committeeInfo.committee_id, committeeInfo.name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.websocket("/ws/{committee_id}")
async def websocket_endpoint(websocket: WebSocket, committee_id: int):
    await manager.connect(websocket, committee_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, committee_id)
