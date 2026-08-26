# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.service as conference_service
import app.session.service as service
from app.auth.dep import get_current_user
from app.auth.service import (
    AuthUser,
    TokenExpiredError,
    TokenInvalidError,
    verify_jwt_token,
)
from app.core.config import Settings, get_settings
from app.core.database import get_db_session
from app.core.dep import get_connection_manager, get_logger, get_session_engine
from app.core.exceptions import AccessDeniedError
from app.session.engine import EventRejectedError, SessionEngine
from app.session.enums import EventErrorCode
from app.session.manager import ConnectionManager
from app.session.models import DispatchOutcome
from app.session.schemas import (
    AuthenticateMessage,
    DispatchResultMessage,
    EventMessage,
    EventRejectedMessage,
    SessionCreationSchema,
)

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Healthcheck route"""
    return Response(status_code=status.HTTP_200_OK)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_session_endpoint(
    session_schema: SessionCreationSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """POST endpoint to create a new session"""
    await conference_service.verify_user_role(
        session=session,
        user_id=current_user.user_id,
        committee_id=session_schema.committee_id,
        required_role="chair",
    )
    session_id = await service.create_session_service(
        session=session,
        session_schema=session_schema,
    )
    return {"id": session_id, "status": "Created"}


@router.post("/{session_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_session_endpoint(
    session_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to activate a planned session"""
    stored = await service.get_session_for_activation(
        session=db_session, committee_session_id=session_id
    )
    await conference_service.verify_user_role(
        session=db_session,
        user_id=current_user.user_id,
        committee_id=stored.committee_id,
        required_role="chair",
    )
    await service.activate_session(
        session=db_session, manager=manager, committee_session_id=session_id
    )


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    engine: Annotated[SessionEngine, Depends(get_session_engine)],
    logger: Annotated[logging.Logger, Depends(get_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """
    Endpoint for connecting to a committee session.

    Overall flow: accepts websocket -> user sends token -> we verify it ->
    if valid, lookup an assigment -> builds actor, connects to manager, and receive The
    current session state
    """

    await websocket.accept()
    try:
        auth_message = await websocket.receive_json()
        validated_auth_data = AuthenticateMessage.model_validate(auth_message)

        # we use pure verify_jwt_token due to websocket not handling bearer-header support
        auth_user = verify_jwt_token(
            settings=settings, token=validated_auth_data.access_token
        )

        session_factory = websocket.app.state.db_session_factory
        async with session_factory() as db:
            assignment = await conference_service.resolve_assignment(
                session=db, user_id=auth_user.user_id, session_id=session_id
            )

            actor = await service.prepare_session_connect(
                session=db,
                manager=manager,
                committee_session_id=session_id,
                assignment=assignment,
            )

        await manager.connect(websocket, session_id, actor)
        try:
            while True:
                data = await websocket.receive_json()
                try:
                    validated_event = EventMessage.model_validate(data)
                except ValidationError:
                    message = EventRejectedMessage(
                        code=EventErrorCode.INVALID_MESSAGE,
                        message="Invalid event message",
                    )
                    await manager.send_message(
                        session_id=session_id, message=message, websocket=websocket
                    )
                    continue

                result = await service.handle_client_messages(
                    manager=manager,
                    engine=engine,
                    logger=logger,
                    session_id=session_id,
                    actor=actor,
                    data=validated_event,
                )
                match result:
                    # Either broadcast result outcome, or send error message back to socket
                    case DispatchOutcome():
                        await manager.broadcast_message(
                            session_id=session_id,
                            message=DispatchResultMessage(
                                state=result.state, effect=result.effect
                            ),
                        )
                    case EventRejectedError():
                        await manager.send_message(
                            session_id=session_id,
                            message=EventRejectedMessage(
                                request_id=validated_event.request_id,
                                code=result.code,
                                message=str(result),
                            ),
                            websocket=websocket,
                        )

        except WebSocketDisconnect:
            manager.disconnect(websocket, session_id)
    except WebSocketDisconnect:
        # this is reached when the ws is disconnected before reaching manager.connect. in this case, just return
        return
    except (
        TokenExpiredError,
        TokenInvalidError,
        AccessDeniedError,
        service.ActorResolutionError,
        service.SessionFetchError,
        ValidationError,
    ) as exc:
        if isinstance(exc, TokenExpiredError):
            reason = "token_expired"
        elif isinstance(exc, TokenInvalidError):
            reason = "token_invalid"
        elif isinstance(exc, AccessDeniedError):
            reason = "access_denied"
        elif isinstance(exc, service.SessionFetchError):
            reason = "session_unavailable"
        elif isinstance(exc, ValidationError):
            reason = "invalid_json"
        else:
            reason = "actor_resolution_error"

        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=reason)
        return
