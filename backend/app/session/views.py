# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, WebSocketException, status
from app.session.models import SessionRole
from app.session.schemas import SessionCreationSchema, DelegateEvents, ChairEvents, SessionEvent
from .manager import manager, SessionLiveState 
from .service import create_session, handle_client_messages, build_actor, ActorResolutionError


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
async def websocket_endpoint(websocket: WebSocket, session_id: int, role: SessionRole, delegation_id: int | None = None, display_name: str | None = None):
    
    try:
        actor = build_actor(session_id, role, delegation_id, display_name)
    except ActorResolutionError as exc:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason=str(exc))

    await manager.connect(websocket, session_id, actor)
    try:
        while True:
            data = await websocket.receive_text()
            await handle_client_messages(
                    session_id=session_id,
                    actor=actor, 
                    data=data,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

