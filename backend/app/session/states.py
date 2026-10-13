from models import SessionLiveState
import enums

class SessionState:
    
    def enterState(self, state : SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class SetupState(SessionState):
    state_name = enums.States.SETUP

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class RollCallState(SessionState):
    state_name = enums.States.ROLL_CALL

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class OpenGSLState(SessionState):
    state_name = enums.States.OPEN_GSL

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class ClosedGSLState(SessionState):
    state_name = enums.States.CLOSED_GSL

    def __init__(self): 
        ...
    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class ModeratedCaucusState(SessionState):
    state_name = enums.States.MODERATED_CAUCUS

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class UnmoderatedCaucusState(SessionState):
    state_name = enums.States.UNMODERATED_CAUCUS

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class TourDeTableState(SessionState):
    state_name = enums.States.TOUR_DE_TABLE

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...


class VotingExecution(SessionState):
    state_name = enums.States.VOTING_EXECUTION

    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class FinishedState(SessionState):
    state_name = enums.States.VOTING_EXECUTION
    def __init__(self): 
        ...

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class SessionStateMachine:

    current_state : SessionState

    def __init__(self, context: SessionLiveState):
        self.current_state = SetupState()
        self.current_state.enterState(context)

    def transition_to(self, context: SessionLiveState, state: SessionState):
        self.current_state.exitState(context)
        self.current_state = state
        self.current_state.enterState(context)