# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response, status, WebSocketException
from app.session.models import SessionActor, SessionRole
from app.session.schemas import SessionCreationSchema, DelegateEvents, ChairEvents, SessionEvent
from .manager import manager, SessionLiveState 
from .service import create_session, handle_client_messages
from .models import DelegationContext


router = APIRouter()

# Helpers
def build_actor(
        session_id: int, 
        role: SessionRole, 
        delegation_id: int | None = None,
        display_name: str | None = None,
        ) -> SessionActor:

    if role == SessionRole.CHAIR:
        return SessionActor(
                role=SessionRole.CHAIR,
                display_name="Chair",
                )

    if role == SessionRole.DELEGATE:
        if delegation_id is None:
            raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="delegation_id required",
                    )

        state = manager.room_states.get(session_id)
        if state is None:
              raise WebSocketException(
                      code=status.WS_1008_POLICY_VIOLATION,
                      reason="session not found",
                      )

        delegation = next(
                  (d for d in state.delegations if d.id == delegation_id),
                  None,
                  )
        if delegation is None:
              raise WebSocketException(
                      code=status.WS_1008_POLICY_VIOLATION,
                      reason="delegation not found",
                      )

        return SessionActor(
                  role=SessionRole.DELEGATE,
                  delegation=DelegationContext(
                      id=delegation.id,
                      seat=delegation.seat,
                      name=delegation.name,
                      code=delegation.code,
                      ),
                  display_name=delegation.name,
                  )

#Workaround to make FastApi add all the Schemas to the OpenApi file
@router.get("/dummy", status_code=status.HTTP_404_NOT_FOUND)
async def dummy(name: SessionEvent, schemas: SessionLiveState, enum1: DelegateEvents, enum2: ChairEvents):
    return Response(status_code=status.HTTP_404_NOT_FOUND)
    

# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_session_endpoint(session_schema: SessionCreationSchema): 
    # Mock a session being created
    create_session(session_schema)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, role: SessionRole, delegation_id: int | None = None, display_name: str | None = None):

    actor = build_actor(session_id, role, delegation_id, display_name)
    await manager.connect(websocket, session_id, actor)
    try:
        while True:
            data = await websocket.receive_text()
            await handle_client_messages(
                    session_id=session_id,
                    actor=actor, 
                    data=data,
            )
            # add broadcast state here if needed?

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

