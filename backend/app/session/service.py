# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

from datetime import datetime, timedelta, timezone 
from .manager import manager, SessionLiveState 

def create_session(session_id: int, name: str):
    # this defines a birthtime
    pass

