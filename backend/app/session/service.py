# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

from datetime import datetime, timedelta, timezone 
from .manager import manager, SessionLiveState 
from .schemas import *
import logging
import json

def create_session(session_id: int, name: str):
    # this defines a birthtime
    pass

uvicorn_logger = logging.getLogger("uvicorn.error")

def handle_client_messages(data: str):
    obj = json.loads(data)
    type = globals().get(obj["type"]) #Get Corresponding Schema
    # TODO: change this to use an event dispatch table or something related so IDE doesnt complain
    parsed = type.model_validate(obj) #Reason Json as correct Object

    uvicorn_logger.info(parsed) #Debugging
    #TODO: depending on typename call a function from engine
    pass
