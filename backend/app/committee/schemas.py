from pydantic import BaseModel
from datetime import datetime 

class CommitteeCreationSchema(BaseModel):
    committee_id: int
    name: str

class CommitteeStateSchema(BaseModel):
    committee_id: int 
    name: str
    current_speaker: int | None 
    timer_end: datetime | None 


CommitteeCreationSchema.model_rebuild()
