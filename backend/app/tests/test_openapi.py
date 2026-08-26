from app.main import app


def test_openapi_exports_websocket_contracts_without_dummy_route() -> None:
    app.openapi_schema = None

    schema = app.openapi()
    components = schema["components"]["schemas"]

    assert "/committees/dummy" not in schema["paths"]
    assert components["ChairEvents"]["type"] == "string"
    assert components["DelegateEvents"]["type"] == "string"
    assert components["SessionEvent"]["discriminator"]["propertyName"] == "type"
    assert components["ClientSessionMessage"]["discriminator"]["propertyName"] == "type"
    assert components["ServerSessionMessage"]["discriminator"]["propertyName"] == "type"
