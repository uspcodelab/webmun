from enum import StrEnum


class ConferenceRole(StrEnum):
    OWNER = "owner"
    SECRETARY_GENERAL = "secretary_general"
    DIRECTOR = "director"
    MODERATOR = "moderator"
    RAPPORTEUR = "rapporteur"
    CRISIS_STAFF = "crisis_staff"
    PRESS = "press"
    LOGISTICS = "logistics"
    STAFF = "staff"


class CommitteeRole(StrEnum):
    CHAIR = "chair"
    DELEGATE = "delegate"
    OBSERVER = "observer"
