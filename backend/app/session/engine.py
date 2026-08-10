# where engine lives
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from math import ceil
from typing import Any, TypeAlias

import app.session.enums as enums
import app.session.schemas as schemas

from .enums import (
    ChairEvents,
    DebateTypes,
    DelegateEvents,
    Motions,
    Questions,
    RollCallChoice,
    States,
)
from .models import (
    AgendaItem,
    DebateContext,
    DelegationContext,
    MotionContext,
    QuestionContext,
    RollCallContext,
    SessionActor,
    SessionLiveState,
    VotingContext,
)


# TODO: add better error handling here
class InvalidProceduralMove(Exception):
    pass


# Dispatch tables: alternative to if else chains
MOTIONS_ALLOWED: dict[States, set[Motions]] = {
    States.INITIAL_DEBATE: {
        Motions.CUSTOM_MOTION,
    },
    States.OPEN_GSL: {
        Motions.CHANGE_DEBATE_TYPE,
        Motions.POSTPONE_SESSION,
        Motions.TOUR_DE_TABLE,
        Motions.END_DEBATE,
        Motions.VOTE_AMENDMENT,
        Motions.VOTE_BY_ROLL_CALL,
        Motions.CLOSE_SPEAKERS_LIST,
        Motions.SPLIT_PROPOSAL,
        Motions.INTRODUCE_RESOLUTION_PROPOSAL,
        Motions.INTRODUCE_AMENDMENT_PROPOSAL,
        Motions.CHANGE_TOPIC,
        Motions.QUORUM,
        Motions.CUSTOM_MOTION,
    },
    States.CLOSED_GSL: {
        Motions.REOPEN_SPEAKERS_LIST,
        Motions.END_DEBATE,
        Motions.VOTE_AMENDMENT,
        Motions.VOTE_BY_ROLL_CALL,
        Motions.INTRODUCE_RESOLUTION_PROPOSAL,
        Motions.INTRODUCE_AMENDMENT_PROPOSAL,
        Motions.QUORUM,
        Motions.CUSTOM_MOTION,
    },
    States.VOTING_PREPARATION: {
        Motions.VOTE_BY_ROLL_CALL,
        Motions.SPLIT_PROPOSAL,
        Motions.CUSTOM_MOTION,
    },
    States.MODERATED_CAUCUS: {
        Motions.POSTPONE_SESSION,
        Motions.END_DEBATE,
        Motions.QUORUM,
        Motions.CUSTOM_MOTION,
    },
    States.UNMODERATED_CAUCUS: {
        Motions.POSTPONE_SESSION,
        Motions.END_DEBATE,
        Motions.QUORUM,
    },
}


# Validations and helpers
def generate_next_motion_id(state: SessionLiveState) -> int:
    if not hasattr(state, "_motion_id_counter"):
        state._motion_id_counter = 0
    state._motion_id_counter += 1
    return state._motion_id_counter


def generate_next_question_id(state: SessionLiveState) -> int:
    if not hasattr(state, "_question_id_counter"):
        state._question_id_counter = 0
    state._question_id_counter += 1
    return state._question_id_counter


def validate_motion_payload(
    payload: schemas.MotionPayload, state: SessionLiveState
) -> None:
    """Should validate motion payload before submitting"""

    # can also raise error if there are missing fields
    if (
        payload.type in {States.MODERATED_CAUCUS}
        and payload.per_speaker_seconds is None
    ):
        raise InvalidProceduralMove("Cannot submit motion without speaking time")


def count_present_delegations(state: SessionLiveState) -> int:
    """Count total present delegations.
    A delegation is considered present (even if AFK)
    if it's Roll Call Choice is Present / Present and Voting"""
    if state.voting_choice is None:
        return 0

    return len(
        [
            True
            for _, vote in state.voting_choice.items()
            if vote == enums.RollCallChoice.PRESENT
            or vote == enums.RollCallChoice.PRESENT_AND_VOTING
        ]
    )


def needs_simple_majority_type(motion: enums.Motions) -> bool:
    """Simple map for majority type. Used when creating VotingContext and tallying votes"""
    qualified_motions = (
        Motions.POSTPONE_SESSION,
        Motions.CHANGE_DEBATE_TYPE,
        Motions.TOUR_DE_TABLE,
        Motions.CLOSE_SPEAKERS_LIST,
        Motions.SPLIT_PROPOSAL,
    )

    if motion not in qualified_motions:
        return True
    return False


def tally_votes(voting: VotingContext, total_presents: int) -> bool:
    """Helper for computing votes.
    Unless motion is explicitly requiring qualified majority,
    will use simple majority (also counts for informal votes)"""
    if total_presents == 0:
        return False

    simple = ceil(total_presents / 2)
    qualified = ceil(0.66 * total_presents)
    in_favor_count = len(
        [
            True
            for _, vote in voting.voting_registry.items()
            if vote == enums.VotingChoice.FAVOUR
        ]
    )
    motion = voting.motion_in_vote

    if motion is None:
        return in_favor_count >= simple

    if (
        needs_simple_majority_type(motion.type)
        and in_favor_count >= simple
        or in_favor_count >= qualified
    ):
        return True

    return False


def get_motion_priority(motion: Motions) -> int | None:
    """Given a motion, return it's priority.
    Some motions are tied. Ex: Change Debate and Tour de Table"""
    priority_map = {
        Motions.POSTPONE_SESSION: 1,
        Motions.REOPEN_SESSION: 2,
        Motions.CHANGE_DEBATE_TYPE: 3,
        Motions.TOUR_DE_TABLE: 3,
        Motions.END_DEBATE: 4,
        Motions.VOTE_AMENDMENT: 4,
        Motions.CLOSE_SPEAKERS_LIST: 5,
        Motions.REOPEN_SPEAKERS_LIST: 5,
        Motions.SPLIT_PROPOSAL: 6,
        Motions.INTRODUCE_RESOLUTION_PROPOSAL: 7,
        Motions.INTRODUCE_AMENDMENT_PROPOSAL: 8,
        Motions.VOTE_BY_ROLL_CALL: 9,
        Motions.QUORUM: 10,
        Motions.CHANGE_TOPIC: 11,
        Motions.CUSTOM_MOTION: 12,
    }

    return priority_map.get(motion)


def get_question_priority(question: Questions) -> int | None:
    """Given a question, return it's priority"""
    priority_map = {
        Questions.PERSONAL_PRIVILEGE: 1,
        Questions.ORDER: 2,
        Questions.QUESTION: 3,
    }

    return priority_map.get(question)


def get_default_speaker_seconds(state: SessionLiveState) -> int | None:
    if state.current_state == States.MODERATED_CAUCUS and state.debate:
        return state.debate.per_speaker_seconds

    if state.current_state in {
        States.OPEN_GSL,
        States.CLOSED_GSL,
        States.INITIAL_DEBATE,
    }:
        return state.gsl_default_time_seconds

    return None


def reset_timer(state: SessionLiveState, seconds: int = 0) -> None:
    state.timer_is_running = False
    state.timer_expiration = None
    state.timer_remaining_seconds = seconds


def require_delegate(actor: SessionActor) -> DelegationContext:
    # helper that returns the delegation context (old Delegation model) while validating
    if actor.role != enums.SessionRole.DELEGATE or actor.delegation is None:
        raise InvalidProceduralMove("Delegate role required")
    return actor.delegation


def require_chair(actor: SessionActor) -> None:
    """Returns"""
    if actor.role != enums.SessionRole.CHAIR:
        raise InvalidProceduralMove("Chair role required")


# -------------- HANDLERS --------------
def handle_delegate_submit_motion(
    state: SessionLiveState, event: schemas.SubmitMotionEvent, actor: SessionActor
) -> SessionLiveState:
    """Handles/Maps all possible states through a motion"""
    require_delegate(actor)

    # Extract payload (as DelegateMotionSchema)
    payload = event.payload
    current_state = state.current_state

    # check if motion can be made for this state
    if payload.type not in MOTIONS_ALLOWED.get(current_state, set()):
        raise InvalidProceduralMove("Cannot submit this motion at this phase")

    if (
        current_state in {States.MODERATED_CAUCUS, States.UNMODERATED_CAUCUS}
        and not state.can_set_motion
    ):
        raise InvalidProceduralMove("Submitting motions during caucuses is disabled")

    validate_motion_payload(payload, state)

    context = MotionContext(
        id=generate_next_motion_id(state),
        priority=get_motion_priority(payload.type) or 1,
        type=payload.type,
        timestamp=datetime.now(UTC),
        delegate_id=actor.delegation.id if actor.delegation is not None else None,
        debate_type=payload.debate_type,
        total_duration_minutes=payload.total_duration_minutes,
        per_speaker_seconds=payload.per_speaker_seconds,
        target_topic=payload.target_topic,
        details=payload.details,
    )

    state.submitted_motions.append(context)
    return state


def handle_submit_question(
    state: SessionLiveState, event: schemas.SubmitQuestionEvent, actor: SessionActor
) -> SessionLiveState:
    require_delegate(actor)

    payload = event.payload

    context = QuestionContext(
        id=generate_next_question_id(state),
        priority=get_question_priority(payload.type) or 1,
        type=payload.type,
        delegate_id=actor.delegation.id,  # type:ignore since require_delegate assumes actor delegate is not none
        details=payload.details,
    )
    state.submitted_questions.append(context)
    return state


def handle_join_queue(
    state: SessionLiveState, event: schemas.JoinQueueEvent, actor: SessionActor
) -> SessionLiveState:
    delegate = require_delegate(actor)

    if state.current_state != States.OPEN_GSL:
        raise InvalidProceduralMove("Cannot enter queue right now")

    # if already in queue, return error, else remove from queue and return state
    if delegate.id in state.gsl_queue:
        raise InvalidProceduralMove("Already in Queue")

    state.gsl_queue.append(delegate.id)
    return state


def handle_leave_queue(
    state: SessionLiveState, event: schemas.LeaveQueueEvent, actor: SessionActor
) -> SessionLiveState:
    delegate = require_delegate(actor)

    if state.current_state != States.OPEN_GSL:
        raise InvalidProceduralMove("Cannot enter queue right now")

    if delegate.id not in state.gsl_queue:
        raise InvalidProceduralMove("Not in Queue")

    state.gsl_queue.remove(delegate.id)
    return state


def handle_cast_vote(
    state: SessionLiveState, event: schemas.CastVoteEvent, actor: SessionActor
) -> SessionLiveState:
    delegate = require_delegate(actor)

    voting_context = state.voting
    if voting_context is None:
        raise InvalidProceduralMove("Cannot vote during this stage")

    # initial voting workflow, may be reviewed later
    # TODO: perhaps allow casting another vote if first one fails
    if delegate.id in voting_context.voting_registry:
        raise InvalidProceduralMove("Already cast vote")

    # register vote on voting context
    voting_context.voting_registry[delegate.id] = event.payload.vote

    return state


def handle_answer_roll_call(
    state: SessionLiveState, event: schemas.AnswerRollCallEvent, actor: SessionActor
) -> SessionLiveState:
    delegate = require_delegate(actor)

    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Roll call not available now")

    state.roll_call.registry[delegate.id] = event.payload.choice
    return state


# Chair events
def handle_open_session(
    state: SessionLiveState, event: schemas.OpenSessionEvent, actor: SessionActor
) -> SessionLiveState:

    require_chair(actor)
    if state.current_state != States.SETUP:
        raise InvalidProceduralMove("Session can only be opened from setup")

    state.current_state = States.ROLL_CALL
    state.roll_call = RollCallContext(registry={})
    state.voting_choice = {}
    state.gsl_queue = []
    state.current_speaker = None
    state.debate = None
    state.timer_is_running = False
    state.timer_expiration = None
    state.timer_remaining_seconds = 0

    return state


def handle_close_session(
    state: SessionLiveState, event: schemas.CloseSessionEvent, actor: SessionActor
) -> SessionLiveState:

    require_chair(actor)

    if (
        state.current_state not in (States.SETUP, States.ROLL_CALL, States.FINISHED)
    ):  # idk what state is best to allow closing session, but for now i'll allow closing from any state other than SETUP, ROLl_CALL and FINISHED itself
        raise InvalidProceduralMove("Session can only be opened from setup")

    state.current_state = States.FINISHED
    state.current_speaker = None
    state.gsl_queue = []  # I'm supposing this queue has the first element popped when someone speaks, so it should be empty when session is closed. In case this list is to be kept, we can remove this line.
    state.can_set_motion = False
    state.debate = None  # Same as queue
    state.timer_is_running = False
    state.timer_expiration = None
    state.timer_remaining_seconds = 0

    return state


# TODO: create helpers for timers -> stop_timer, set_timer, pause_timer, etc
def handle_toggle_timer(
    state: SessionLiveState, event: schemas.ToggleTimerEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    # uses utc for now
    now = datetime.now(UTC)
    if state.timer_is_running:
        # timer currently running
        if state.timer_expiration is not None and now > state.timer_expiration:
            # currently overtime, act as stop button

            state.timer_is_running = False
            state.timer_remaining_seconds = 0

        elif state.timer_expiration is not None:
            state.timer_is_running = False
            elapsed = state.timer_expiration - now
            state.timer_remaining_seconds = int(elapsed.total_seconds())
            state.timer_expiration = None
    else:
        # timer currently stopped
        state.timer_is_running = True
        state.timer_expiration = now + timedelta(seconds=state.timer_remaining_seconds)

    return state


def handle_increase_timer(
    state: SessionLiveState, event: schemas.IncreaseTimerEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    now = datetime.now(UTC)

    if state.timer_is_running and state.timer_expiration is not None:
        state.timer_expiration += timedelta(seconds=event.payload.seconds)
        state.timer_remaining_seconds = int(
            (state.timer_expiration - now).total_seconds()
        )
    else:
        state.timer_remaining_seconds += event.payload.seconds

    return state


def handle_open_informal_voting(
    state: SessionLiveState, event: schemas.OpenInformalVotingEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    if state.current_state == States.VOTING_EXECUTION:
        raise InvalidProceduralMove(
            "Can't open voting while another voting is in course"
        )

    state.voting = VotingContext(
        target_type=enums.VotingType.INFORMAL,
        title=event.payload.title,
        return_state=state.current_state,
        voting_registry={},
    )

    state.current_state = States.VOTING_EXECUTION

    return state


def handle_close_informal_voting(
    state: SessionLiveState,
    event: schemas.CloseInformalVotingEvent,
    actor: SessionActor,
) -> SessionLiveState:
    require_chair(actor)

    if state.voting is None:
        raise InvalidProceduralMove("No voting present")

    if (
        state.current_state != States.VOTING_EXECUTION
        or state.voting.target_type != enums.VotingType.INFORMAL
    ):
        raise InvalidProceduralMove("Can't close voting")

    # extract last state
    state.current_state = state.voting.return_state

    state.voting = None

    return state


def apply_passed_motion(
    state: SessionLiveState, motion: MotionContext, return_state: States
) -> None:
    """Apply a passed procedural motion to the live session state in place."""
    next_state = return_state  # as fallback
    state.current_speaker = None
    state.timer_is_running = False
    state.timer_expiration = None

    # 1st block: change of debate motions
    if motion.type == Motions.CHANGE_DEBATE_TYPE and motion.debate_type is not None:
        state.caucus_list = []
        state.current_speaker = None
        duration_seconds = (
            (motion.total_duration_minutes * 60)
            if motion.total_duration_minutes is not None
            else 600
        )  # defaults to 10 minutes as fallback

        match motion.debate_type:
            case DebateTypes.MODERATED_DEBATE:
                next_state = States.MODERATED_CAUCUS
                state.debate = DebateContext(
                    debate_type=DebateTypes.MODERATED_DEBATE,
                    return_state=return_state,
                    total_duration_seconds=duration_seconds,
                    per_speaker_seconds=motion.per_speaker_seconds,
                    expires_at=datetime.now(UTC) + timedelta(seconds=duration_seconds),
                )
                reset_timer(
                    state,
                    motion.per_speaker_seconds
                    if motion.per_speaker_seconds is not None
                    else 60,
                )

            case DebateTypes.UNMODERATED_DEBATE:
                next_state = States.UNMODERATED_CAUCUS
                state.debate = DebateContext(
                    debate_type=DebateTypes.UNMODERATED_DEBATE,
                    return_state=return_state,
                    total_duration_seconds=duration_seconds,
                    per_speaker_seconds=None,
                    expires_at=datetime.now(UTC) + timedelta(seconds=duration_seconds),
                )
                reset_timer(state)  # should not display per_speaker timer

            case DebateTypes.SPEAKERS_LIST:
                next_state = States.OPEN_GSL
                state.debate = None
                reset_timer(state, state.gsl_default_time_seconds)

            case _:
                raise InvalidProceduralMove("Undefined debate type")

    match motion.type:
        case Motions.POSTPONE_SESSION:
            pass
        case Motions.REOPEN_SESSION:
            pass
        case Motions.TOUR_DE_TABLE:
            next_state = States.TOUR_DE_TABLE
            state.caucus_list = [
                del_id
                for del_id, choice in state.roll_call.registry.items()
                if choice
                in (
                    enums.RollCallChoice.PRESENT,
                    enums.RollCallChoice.PRESENT_AND_VOTING,
                )
            ]

        case Motions.END_DEBATE:
            # clean gsl list
            state.gsl_queue = []
            state.debate = None
            reset_timer(state)
            next_state = States.VOTING_PROCEDURES  # or VOTING_PREPARATION

        case Motions.VOTE_AMENDMENT:
            # note: seems more like an informal consultation
            pass
        case Motions.VOTE_BY_ROLL_CALL:
            # will define the VotingContext for resolutions
            pass
        case Motions.CLOSE_SPEAKERS_LIST:
            next_state = States.CLOSED_GSL

        case Motions.REOPEN_SPEAKERS_LIST:
            next_state = States.OPEN_GSL

        case Motions.SPLIT_PROPOSAL:
            # note: seems more like an informal consultation
            pass
        case Motions.CHANGE_TOPIC:
            # note: seems more like an informal consultation
            pass
        case Motions.QUORUM:
            state.roll_call = RollCallContext(registry={}, return_state=return_state)
            next_state = States.ROLL_CALL
        case _:
            raise InvalidProceduralMove("Undefined motion type")

    # additional case: if we went from GSL to something, save gsl structures
    state.current_state = next_state


def handle_close_procedural_voting(
    state: SessionLiveState,
    event: schemas.CloseProceduralVotingEvent,
    actor: SessionActor,
) -> SessionLiveState:
    require_chair(actor)

    if state.voting is None:
        raise InvalidProceduralMove("No voting present")

    if (
        state.current_state != States.VOTING_EXECUTION
        or state.voting.target_type != enums.VotingType.PROCEDURAL
    ):
        raise InvalidProceduralMove("Can't close voting")

    motion = state.voting.motion_in_vote

    if motion is None:
        raise InvalidProceduralMove("Can't close voting if motion is None")

    present = count_present_delegations(state)
    passed = tally_votes(state.voting, present)

    if passed:
        apply_passed_motion(state, motion, return_state=state.voting.return_state)
    else:
        # motion failed, so return to last state
        state.current_state = state.voting.return_state

    # clear state voting
    state.voting = None
    return state


def handle_finish_caucus(
    state: SessionLiveState, event: schemas.FinishCaucusEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    if state.debate is None or state.current_state not in {
        States.MODERATED_CAUCUS,
        States.UNMODERATED_CAUCUS,
    }:
        raise InvalidProceduralMove("No active caucus")

    return_state = state.debate.return_state
    state.current_speaker = None
    state.caucus_list = []
    state.debate = None
    reset_timer(state)
    state.current_state = return_state
    return state


# handles setting state into VOTING_EXECUTION or rejecting the motion
def handle_resolve_motion(
    state: SessionLiveState, event: schemas.ResolveMotionEvent, actor: SessionActor
) -> SessionLiveState:
    # TODO: check how to resolve INTRODUCE_RESOLUTION_PROPOSAL and INTRODUCE_AMENDMENT_PROPOSAL motions separately from procedural motions
    require_chair(actor)

    payload = event.payload
    # next() function with generator expression
    motion = next(
        (m for m in state.submitted_motions if m.id == payload.motion_id), None
    )

    if motion is None:
        raise InvalidProceduralMove("Motion not found")

    majority_type = (
        enums.MajorityTypes.SIMPLE
        if needs_simple_majority_type(motion.type)
        else enums.MajorityTypes.QUALIFIED
    )

    if payload.action:
        state.voting = VotingContext(
            target_type=enums.VotingType.PROCEDURAL,
            motion_in_vote=motion,
            return_state=state.current_state,
            voting_registry={},
            majority=majority_type,
        )

        state.current_state = States.VOTING_EXECUTION

    state.submitted_motions.remove(motion)

    return state


def handle_chair_submit_motion(
    state: SessionLiveState, event: schemas.LogMotionEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    payload = event.payload
    validate_motion_payload(payload=payload, state=state)

    # create motion context
    context = MotionContext(
        id=generate_next_motion_id(state),
        priority=get_motion_priority(payload.type) or 1,
        type=payload.type,
        timestamp=datetime.now(UTC),
        delegate_id=payload.representation_id,
        debate_type=payload.debate_type,
        total_duration_minutes=payload.total_duration_minutes,
        per_speaker_seconds=payload.per_speaker_seconds,
        target_topic=payload.target_topic,
        details=payload.details,
    )

    majority_type = (
        enums.MajorityTypes.SIMPLE
        if needs_simple_majority_type(payload.type)
        else enums.MajorityTypes.QUALIFIED
    )

    # set state to be in voting execution
    state.voting = VotingContext(
        target_type=enums.VotingType.PROCEDURAL,
        motion_in_vote=context,
        return_state=state.current_state,
        voting_registry={},
        majority=majority_type,
    )

    state.current_state = States.VOTING_EXECUTION
    return state


def handle_set_agenda(
    state: SessionLiveState, event: schemas.SetAgendaEvent, actor: SessionActor
) -> SessionLiveState: ...


def handle_mark_agenda_item(
    state: SessionLiveState, event: schemas.MarkAgendaItemEvent, actor: SessionActor
) -> SessionLiveState:
    if event.payload.discussed is not None:
        state.agenda_topics[
            event.payload.index
        ].already_discussed = event.payload.discussed
    if event.payload.indiscussion is not None:
        if event.payload.indiscussion:
            state.active_topic_index = event.payload.index
        else:
            state.active_topic_index = None
    return state


def handle_set_agenda_item(
    state: SessionLiveState, event: schemas.SetAgendaItemEvent, actor: SessionActor
) -> SessionLiveState:
    item = AgendaItem(
        index=event.payload.index, topic=event.payload.topic, already_discussed=False
    )
    state.agenda_topics[event.payload.index] = item
    return state


def handle_delete_agenda_item(
    state: SessionLiveState, event: schemas.DeleteAgendaItemEvent, actor: SessionActor
) -> SessionLiveState:

    state.agenda_topics.pop(event.payload.index)

    if state.active_topic_index == event.payload.index:
        state.active_topic_index = None
    return state


def handle_manual_phase_set(
    state: SessionLiveState, event: schemas.SetPhaseEvent, actor: SessionActor
) -> SessionLiveState: ...


def handle_next_speaker(
    state: SessionLiveState, event: schemas.NextSpeakerEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    if state.current_state in {States.OPEN_GSL, States.CLOSED_GSL}:
        if not state.gsl_queue:
            state.current_speaker = None
            reset_timer(state)
            return state
        state.current_speaker = state.gsl_queue.pop(0)
        reset_timer(state, state.gsl_default_time_seconds)
        return state

    if state.current_state == States.TOUR_DE_TABLE:
        if not state.caucus_list:
            state.current_speaker = None
            reset_timer(state)
            return state
        state.current_speaker = state.caucus_list.pop(0)
        reset_timer(state, state.gsl_default_time_seconds)
        return state

    if state.current_state == States.MODERATED_CAUCUS:
        raise InvalidProceduralMove("Chair must grant floor during moderated caucus")

    raise InvalidProceduralMove("Cannot advance speaker right now")


def handle_add_gsl_speaker(
    state: SessionLiveState, event: schemas.AddGslSpeakerEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    if state.current_state not in {States.OPEN_GSL, States.CLOSED_GSL}:
        raise InvalidProceduralMove("Can only add speakers to the GSL")

    representation_id = event.payload.representation_id
    if representation_id not in state.delegations:
        raise InvalidProceduralMove("Representation not found")
    if representation_id in state.gsl_queue:
        raise InvalidProceduralMove("Representation already in GSL queue")

    state.gsl_queue.append(representation_id)
    return state


def handle_grant_floor(
    state: SessionLiveState, event: schemas.GrantFloorEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)

    representation_id = event.payload.representation_id
    if representation_id not in state.delegations:
        raise InvalidProceduralMove("Representation not found")

    if state.current_state in {States.OPEN_GSL, States.CLOSED_GSL}:
        if representation_id in state.gsl_queue:
            state.gsl_queue.remove(representation_id)
        seconds = event.payload.seconds or state.gsl_default_time_seconds
    elif state.current_state == States.MODERATED_CAUCUS:
        if state.debate is None:
            raise InvalidProceduralMove("No active moderated caucus")
        seconds = event.payload.seconds or state.debate.per_speaker_seconds or 60
    elif state.current_state == States.TOUR_DE_TABLE:
        if representation_id in state.caucus_list:
            state.caucus_list.remove(representation_id)
        seconds = event.payload.seconds or state.gsl_default_time_seconds
    elif state.current_state == States.UNMODERATED_CAUCUS:
        raise InvalidProceduralMove("Cannot grant floor during unmoderated caucus")
    else:
        raise InvalidProceduralMove("Cannot grant floor right now")

    state.current_speaker = representation_id
    reset_timer(state, seconds)

    return state


def handle_mark_roll_call(
    state: SessionLiveState, event: schemas.MarkRollCallEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Cannot mark roll call right now")

    if event.payload.delegation_id not in state.delegations:
        raise InvalidProceduralMove("Delegation does not exist")

    state.roll_call.registry[event.payload.delegation_id] = event.payload.choice

    return state


def handle_mark_roll_call_bulk(
    state: SessionLiveState, event: schemas.MarkRollCallBulkEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Cannot mark roll call right now")

    for delegation_id in event.payload.Rollcalls.keys():
        if delegation_id not in state.delegations:
            raise InvalidProceduralMove("One delegation does not exist")

    state.roll_call.registry.update(event.payload.Rollcalls)

    return state


def handle_close_roll_call(
    state: SessionLiveState, event: schemas.CloseRollCallEvent, actor: SessionActor
) -> SessionLiveState:
    require_chair(actor)
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Cannot close roll call right now")

    # mark all delegations as absent in the first case. This will enable us to use
    # RollCallContext to tally votes
    for delegation_id in state.delegations:
        state.roll_call.registry.setdefault(delegation_id, RollCallChoice.ABSENT)

    # Initial roll call enters Open GSL; quorum roll calls restore their source state.
    state.current_state = state.roll_call.return_state or States.OPEN_GSL
    state.voting_choice = {
        delegation_id: RollCallChoice.PRESENT_AND_VOTING
        if choice == RollCallChoice.PRESENT_AND_VOTING
        else RollCallChoice.PRESENT
        for delegation_id, choice in state.roll_call.registry.items()
        if choice in {RollCallChoice.PRESENT, RollCallChoice.PRESENT_AND_VOTING}
    }
    return state


# Signature for events/handlers, uses legacy(ish) 3.11 TypeAlias
EventHandler: TypeAlias = Callable[
    [SessionLiveState, Any, SessionActor],  # overall signature
    SessionLiveState,  # Return type
]

EVENT_HANDLERS: dict[DelegateEvents | ChairEvents, EventHandler] = {
    DelegateEvents.SUBMIT_MOTION: handle_delegate_submit_motion,
    DelegateEvents.SUBMIT_QUESTION: handle_submit_question,
    DelegateEvents.JOIN_QUEUE: handle_join_queue,
    DelegateEvents.LEAVE_QUEUE: handle_leave_queue,
    DelegateEvents.CAST_VOTE: handle_cast_vote,
    DelegateEvents.ANSWER_ROLLCALL: handle_answer_roll_call,
    ChairEvents.OPEN_SESSION: handle_open_session,
    ChairEvents.INCREASE_TIMER: handle_increase_timer,
    ChairEvents.TOGGLE_TIMER: handle_toggle_timer,
    ChairEvents.OPEN_INFORMAL_VOTING: handle_open_informal_voting,
    ChairEvents.CLOSE_INFORMAL_VOTING: handle_close_informal_voting,
    ChairEvents.CLOSE_PROCEDURAL_VOTING: handle_close_procedural_voting,
    ChairEvents.FINISH_CAUCUS: handle_finish_caucus,
    ChairEvents.RESOLVE_MOTION: handle_resolve_motion,
    ChairEvents.LOG_MOTION: handle_chair_submit_motion,
    ChairEvents.SET_AGENDA: handle_set_agenda,
    ChairEvents.SET_AGENDA_ITEM: handle_set_agenda_item,
    ChairEvents.MARK_AGENDA_ITEM: handle_mark_agenda_item,
    ChairEvents.DELETE_AGENDA_ITEM: handle_delete_agenda_item,
    ChairEvents.MANUAL_PHASE_SET: handle_manual_phase_set,
    ChairEvents.CLOSE_SESSION: handle_close_session,
    ChairEvents.NEXT_SPEAKER: handle_next_speaker,
    ChairEvents.ADD_GSL_SPEAKER: handle_add_gsl_speaker,
    ChairEvents.GRANT_FLOOR: handle_grant_floor,
    ChairEvents.MARK_ROLLCALL: handle_mark_roll_call,
    ChairEvents.MARK_ROLLCALL_BULK: handle_mark_roll_call_bulk,
    ChairEvents.CLOSE_ROLLCALL: handle_close_roll_call,
}


class SessionEngine:
    # function to calculate new state over old one
    def dispatch(
        self, state: SessionLiveState, event: schemas.SessionEvent, actor: SessionActor
    ) -> SessionLiveState:

        handler = EVENT_HANDLERS.get(event.type)
        if handler is None:
            raise InvalidProceduralMove(f"Unsupported Type: {event.type}")

        return handler(state, event, actor)
