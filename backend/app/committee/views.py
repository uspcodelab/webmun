from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status
import asyncio
from app.committee.schemas import CommitteeStateSchema, CommitteeCreationSchema
from .manager import manager

router = APIRouter()

# Mock db
live_committees = {}

# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_commitee(committeeInfo: CommitteeCreationSchema):
    # Mock a committee being created
    live_committees[committeeInfo.committee_id] = {"name": committeeInfo.name}
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# Initial endpoint for getting info about the session
# This should be HTTP for now, and should give info
@router.get("/{committee_id}/session")
async def view_session(committee_id: int):
    return live_committees[committee_id]

@router.websocket("/ws/{committee_id}")
async def websocket_endpoint(websocket: WebSocket, committee_id: int):
    await manager.connect(websocket, committee_id)
    try:
        count = 0
        while True:
            await websocket.send_json({"type": "TICK", "value": count})
            count += 1
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, committee_id)
