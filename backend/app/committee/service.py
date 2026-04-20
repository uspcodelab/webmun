from datetime import datetime, timedelta, timezone 
from .manager import manager, CommitteeLiveState

def create_committee(committee_id: int, name: str):
    # this defines a birthtime
    start_time = datetime.now(timezone.utc)
    state_info = CommitteeLiveState(
            committee_id=committee_id,
            committee_name=name,
            start_time=start_time,
    )

    manager.room_states[committee_id] = state_info 
    return state_info

# more things can be done here, like a trigger timer 
