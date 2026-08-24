from typing import Any

from pydantic import TypeAdapter

from app.session.enums import ChairEvents, DelegateEvents
from app.session.schemas import (
    ClientSessionMessage,
    ServerSessionMessage,
    SessionEvent,
)


def add_websocket_message_schemas(openapi_schema: dict[str, Any]) -> None:
    """Add WebSocket-only message contracts to the generated OpenAPI document.

    FastAPI only discovers schemas referenced by HTTP routes. These contracts are
    validated on the WebSocket endpoint, so export them explicitly instead of
    maintaining a fake HTTP route solely for schema generation.
    """
    components = openapi_schema.setdefault("components", {}).setdefault(
        "schemas", {}
    )

    for name, message_type in {
        "ChairEvents": ChairEvents,
        "DelegateEvents": DelegateEvents,
        "SessionEvent": SessionEvent,
        "ClientSessionMessage": ClientSessionMessage,
        "ServerSessionMessage": ServerSessionMessage,
    }.items():
        schema = TypeAdapter(message_type).json_schema(
            ref_template="#/components/schemas/{model}"
        )
        definitions = schema.pop("$defs", {})
        components.update(definitions)
        components[name] = schema
