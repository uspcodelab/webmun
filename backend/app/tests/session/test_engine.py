from datetime import UTC, datetime

import pytest

import app.session.engine as eng
import app.session.enums as enums
import app.session.models as md
import app.session.schemas as sch


@pytest.fixture
def open_gsl_state(session_state: md.SessionLiveState) -> md.SessionLiveState:
    session_state.current_state = enums.States.OPEN_GSL
    return session_state


@pytest.fixture
def informal_voting_state(session_state: md.SessionLiveState) -> md.SessionLiveState:
    session_state.current_state = enums.States.VOTING_EXECUTION
    session_state.voting = md.VotingContext(
        target_type=enums.VotingType.INFORMAL,
        return_state=enums.States.OPEN_GSL,
        voting_registry={},
    )
    return session_state


@pytest.fixture
def submit_debate_motion_event(
    delegate_actor: md.SessionActor,
) -> sch.SubmitMotionEvent:
    return sch.SubmitMotionEvent(
        type=enums.DelegateEvents.SUBMIT_MOTION,
        payload=sch.DelegateMotionPayload(
            type=enums.Motions.CHANGE_DEBATE_TYPE,
            debate_type=enums.DebateTypes.MODERATED_DEBATE,
            total_duration_minutes=10,
            per_speaker_seconds=60,
        ),
    )


@pytest.fixture
def log_motion_event(chair_actor: md.SessionActor) -> sch.LogMotionEvent:
    return sch.LogMotionEvent(
        type=enums.ChairEvents.LOG_MOTION,
        payload=sch.ChairMotionPayload(
            type=enums.Motions.CHANGE_DEBATE_TYPE,
            debate_type=enums.DebateTypes.MODERATED_DEBATE,
            total_duration_minutes=10,
            per_speaker_seconds=60,
            representation_id=1,
            decision=enums.MotionDecision.ACCEPT,
        ),
    )


@pytest.fixture
def submit_question_event(delegate_actor: md.SessionActor) -> sch.SubmitQuestionEvent:
    return sch.SubmitQuestionEvent(
        type=enums.DelegateEvents.SUBMIT_QUESTION,
        payload=sch.DelegateQuestionPayload(
            type=enums.Questions.PERSONAL_PRIVILEGE,
            delegate=delegate_actor.delegation.id,  # type: ignore[union-attr]
            details="Need technical assistance.",
        ),
    )


@pytest.fixture
def join_queue_event() -> sch.JoinQueueEvent:
    return sch.JoinQueueEvent(type=enums.DelegateEvents.JOIN_QUEUE, payload={})


@pytest.fixture
def leave_queue_event() -> sch.LeaveQueueEvent:
    return sch.LeaveQueueEvent(type=enums.DelegateEvents.LEAVE_QUEUE, payload={})


@pytest.fixture
def cast_vote_event() -> sch.CastVoteEvent:
    return sch.CastVoteEvent(
        type=enums.DelegateEvents.CAST_VOTE,
        payload=sch.DelegateVotingPayload(vote=enums.VotingChoice.FAVOUR),
    )


@pytest.fixture
def answer_roll_call_event() -> sch.AnswerRollCallEvent:
    return sch.AnswerRollCallEvent(
        type=enums.DelegateEvents.ANSWER_ROLLCALL,
        payload=sch.AnswerRollCallPayload(choice=enums.RollCallChoice.PRESENT),
    )


@pytest.fixture
def close_roll_call_event() -> sch.CloseRollCallEvent:
    return sch.CloseRollCallEvent(
        type=enums.ChairEvents.CLOSE_ROLLCALL,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def toggle_timer_event() -> sch.ToggleTimerEvent:
    return sch.ToggleTimerEvent(
        type=enums.ChairEvents.TOGGLE_TIMER,
        payload=sch.ChairToggleTimerPayload(toggle=True),
    )


@pytest.fixture
def increase_timer_event() -> sch.IncreaseTimerEvent:
    return sch.IncreaseTimerEvent(
        type=enums.ChairEvents.INCREASE_TIMER,
        payload=sch.ChairIncreaseTimerPayload(seconds=15),
    )


@pytest.fixture
def open_informal_voting_event() -> sch.OpenInformalVotingEvent:
    return sch.OpenInformalVotingEvent(
        type=enums.ChairEvents.OPEN_INFORMAL_VOTING,
        payload=sch.ChairOpenInformalVotingPayload(
            title="Straw poll",
            majority=enums.MajorityTypes.SIMPLE,
            veto_power=False,
        ),
    )


@pytest.fixture
def close_informal_voting_event() -> sch.CloseInformalVotingEvent:
    return sch.CloseInformalVotingEvent(
        type=enums.ChairEvents.CLOSE_INFORMAL_VOTING,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def close_procedural_voting_event() -> sch.CloseProceduralVotingEvent:
    return sch.CloseProceduralVotingEvent(
        type=enums.ChairEvents.CLOSE_PROCEDURAL_VOTING,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def finish_caucus_event() -> sch.FinishCaucusEvent:
    return sch.FinishCaucusEvent(
        type=enums.ChairEvents.FINISH_CAUCUS,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def close_speakers_list_motion(
    delegate_actor: md.SessionActor,
) -> md.MotionContext:
    return md.MotionContext(
        id=1,
        priority=1,
        type=enums.Motions.CLOSE_SPEAKERS_LIST,
        timestamp=datetime.now(UTC),
        delegate_id=delegate_actor.delegation.id,  # type: ignore[union-attr]
    )


@pytest.fixture
def reopen_speakers_list_motion(delegate_actor: md.SessionActor) -> md.MotionContext:
    return md.MotionContext(
        id=1,
        priority=1,
        type=enums.Motions.REOPEN_SPEAKERS_LIST,
        timestamp=datetime.now(UTC),
        delegate_id=delegate_actor.delegation.id,  # type: ignore[union-attr]
    )


@pytest.fixture
def procedural_voting_state(
    open_gsl_state: md.SessionLiveState,
    close_speakers_list_motion: md.MotionContext,
) -> md.SessionLiveState:
    open_gsl_state.current_state = enums.States.VOTING_EXECUTION
    open_gsl_state.voting = md.VotingContext(
        target_type=enums.VotingType.PROCEDURAL,
        motion_in_vote=close_speakers_list_motion,
        return_state=enums.States.OPEN_GSL,
        voting_registry={},
    )
    return open_gsl_state


@pytest.fixture
def resolve_motion_event() -> sch.ResolveMotionEvent:
    return sch.ResolveMotionEvent(
        type=enums.ChairEvents.RESOLVE_MOTION,
        payload=sch.ChairResolveMotionPayload(motion_id=1, action=True),
    )


@pytest.fixture
def next_speaker_event() -> sch.NextSpeakerEvent:
    return sch.NextSpeakerEvent(
        type=enums.ChairEvents.NEXT_SPEAKER,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def add_gsl_speaker_event() -> sch.AddGslSpeakerEvent:
    return sch.AddGslSpeakerEvent(
        type=enums.ChairEvents.ADD_GSL_SPEAKER,
        payload=sch.AddGslSpeakerPayload(representation_id=1),
    )


@pytest.fixture
def grant_floor_event() -> sch.GrantFloorEvent:
    return sch.GrantFloorEvent(
        type=enums.ChairEvents.GRANT_FLOOR,
        payload=sch.GrantFloorPayload(representation_id=1, seconds=45),
    )


@pytest.fixture
def mark_roll_call_event() -> sch.MarkRollCallEvent:
    return sch.MarkRollCallEvent(
        type=enums.ChairEvents.MARK_ROLLCALL,
        payload=sch.MarkRollCallPayload(
            delegation_id=1,
            choice=enums.RollCallChoice.PRESENT_AND_VOTING,
        ),
    )


@pytest.fixture
def mark_roll_call_bulk_event() -> sch.MarkRollCallBulkEvent:
    return sch.MarkRollCallBulkEvent(
        type=enums.ChairEvents.MARK_ROLLCALL_BULK,
        payload=sch.MarkRollCallBulkPayload(
            Rollcalls={
                1: enums.RollCallChoice.PRESENT,
                2: enums.RollCallChoice.ABSENT,
            },
        ),
    )


@pytest.fixture
def open_session_event() -> sch.OpenSessionEvent:
    return sch.OpenSessionEvent(
        type=enums.ChairEvents.OPEN_SESSION,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def set_agenda_event() -> sch.SetAgendaEvent:
    return sch.SetAgendaEvent(
        type=enums.ChairEvents.SET_AGENDA,
        payload=sch.ChairSetAgendaPayload(agenda=["Topic A", "Topic B"]),
    )


@pytest.fixture
def manual_phase_set_event() -> sch.SetPhaseEvent:
    return sch.SetPhaseEvent(
        type=enums.ChairEvents.MANUAL_PHASE_SET,
        payload=sch.ChairSetPhasePayload(target_phase=enums.States.OPEN_GSL),
    )


def test_get_motion_priority() -> None:
    motion = enums.Motions.END_DEBATE
    assert eng.get_motion_priority(motion) == 4


def test_get_question_priority() -> None:
    question = enums.Questions.QUESTION
    assert eng.get_question_priority(question) == 3


def test_delegate_can_submit_motion_in_open_gsl(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, submit_debate_motion_event, delegate_actor)

    assert len(state.submitted_motions) == 1
    assert state.submitted_motions[0].id == 1
    assert state.submitted_motions[0].type == enums.Motions.CHANGE_DEBATE_TYPE
    assert state.submitted_motions[0].delegate_id == delegate_actor.delegation.id  # type: ignore[union-attr]


def test_delegate_cannot_submit_motion_outside_allowed_phase(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot submit this motion"):
        engine.dispatch(session_state, submit_debate_motion_event, delegate_actor)


def test_delegate_cannot_submit_chair_motion(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    log_motion_event: sch.LogMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, log_motion_event, delegate_actor)


def test_chair_can_log_motion(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    log_motion_event: sch.LogMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, log_motion_event, chair_actor)
    assert state.current_state == enums.States.VOTING_EXECUTION
    assert state.voting is not None and state.voting.motion_in_vote is not None
    assert state.voting.motion_in_vote.type == log_motion_event.payload.type


def test_chair_cannot_submit_delegate_motion(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Delegate role required"):
        engine.dispatch(open_gsl_state, submit_debate_motion_event, chair_actor)


def test_delegate_can_submit_question(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    submit_question_event: sch.SubmitQuestionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, submit_question_event, delegate_actor)

    assert len(state.submitted_questions) == 1
    assert state.submitted_questions[0].id == 1
    assert state.submitted_questions[0].type == enums.Questions.PERSONAL_PRIVILEGE
    assert state.submitted_questions[0].delegate_id == delegate_actor.delegation.id  # type: ignore[union-attr]


def test_delegate_can_join_queue(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)

    assert state.gsl_queue == [0]


def test_delegate_cannot_join_queue_twice(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)

    with pytest.raises(eng.InvalidProceduralMove, match="Already in Queue"):
        engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)


def test_delegate_cannot_join_queue_outside_open_gsl(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot enter queue"):
        engine.dispatch(session_state, join_queue_event, delegate_actor)


def test_chair_cannot_join_queue(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Delegate role required"):
        engine.dispatch(open_gsl_state, join_queue_event, chair_actor)


def test_delegate_can_leave_queue(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    leave_queue_event: sch.LeaveQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    open_gsl_state.gsl_queue.append(0)

    state = engine.dispatch(open_gsl_state, leave_queue_event, delegate_actor)

    assert state.gsl_queue == []


def test_delegate_cannot_leave_queue_when_not_queued(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    leave_queue_event: sch.LeaveQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Not in Queue"):
        engine.dispatch(open_gsl_state, leave_queue_event, delegate_actor)


def test_delegate_can_cast_vote(
    engine: eng.SessionEngine,
    informal_voting_state: md.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(informal_voting_state, cast_vote_event, delegate_actor)

    assert state.voting is not None
    assert state.voting.voting_registry == {0: enums.VotingChoice.FAVOUR}


def test_delegate_cannot_cast_vote_twice(
    engine: eng.SessionEngine,
    informal_voting_state: md.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    engine.dispatch(informal_voting_state, cast_vote_event, delegate_actor)

    with pytest.raises(eng.InvalidProceduralMove, match="Already cast vote"):
        engine.dispatch(informal_voting_state, cast_vote_event, delegate_actor)


def test_delegate_cannot_cast_vote_without_voting_context(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot vote"):
        engine.dispatch(session_state, cast_vote_event, delegate_actor)


def test_delegate_can_answer_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    answer_roll_call_event: sch.AnswerRollCallEvent,
    delegate_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    state = engine.dispatch(session_state, answer_roll_call_event, delegate_actor)

    assert state.roll_call.registry == {0: enums.RollCallChoice.PRESENT}


def test_chair_can_close_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    close_roll_call_event: sch.CloseRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL
    session_state.roll_call.registry = {
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT_AND_VOTING,
        3: enums.RollCallChoice.ABSENT,
    }

    state = engine.dispatch(session_state, close_roll_call_event, chair_actor)

    assert state.current_state == enums.States.OPEN_GSL
    assert state.roll_call.registry == {
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT_AND_VOTING,
    }


def test_quorum_roll_call_restores_closed_gsl(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    close_roll_call_event: sch.CloseRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.VOTING_EXECUTION
    session_state.roll_call.registry = {
        0: enums.RollCallChoice.PRESENT,
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT,
    }
    session_state.voting = md.VotingContext(
        target_type=enums.VotingType.PROCEDURAL,
        return_state=enums.States.CLOSED_GSL,
        motion_in_vote=md.MotionContext(
            id=1,
            type=enums.Motions.QUORUM,
            timestamp=datetime.now(UTC),
        ),
        voting_registry={
            0: enums.VotingChoice.FAVOUR,
            1: enums.VotingChoice.FAVOUR,
        },
    )

    state = engine.dispatch(session_state, close_procedural_voting_event, chair_actor)

    assert state.current_state == enums.States.ROLL_CALL
    assert state.roll_call.return_state == enums.States.CLOSED_GSL

    state = engine.dispatch(state, close_roll_call_event, chair_actor)

    assert state.current_state == enums.States.CLOSED_GSL


def test_quorum_roll_call_restores_moderated_caucus(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    close_roll_call_event: sch.CloseRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    debate = md.DebateContext(
        debate_type=enums.DebateTypes.MODERATED_DEBATE,
        return_state=enums.States.OPEN_GSL,
        per_speaker_seconds=60,
    )
    session_state.current_state = enums.States.VOTING_EXECUTION
    session_state.debate = debate
    session_state.roll_call.registry = {
        0: enums.RollCallChoice.PRESENT,
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT,
    }
    session_state.voting = md.VotingContext(
        target_type=enums.VotingType.PROCEDURAL,
        return_state=enums.States.MODERATED_CAUCUS,
        motion_in_vote=md.MotionContext(
            id=1,
            type=enums.Motions.QUORUM,
            timestamp=datetime.now(UTC),
        ),
        voting_registry={
            0: enums.VotingChoice.FAVOUR,
            1: enums.VotingChoice.FAVOUR,
        },
    )

    state = engine.dispatch(session_state, close_procedural_voting_event, chair_actor)
    state = engine.dispatch(state, close_roll_call_event, chair_actor)

    assert state.current_state == enums.States.MODERATED_CAUCUS
    assert state.debate == debate


def test_delegate_cannot_close_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    close_roll_call_event: sch.CloseRollCallEvent,
    delegate_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, close_roll_call_event, delegate_actor)


def test_chair_can_toggle_timer(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    toggle_timer_event: sch.ToggleTimerEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.timer_remaining_seconds = 30

    state = engine.dispatch(session_state, toggle_timer_event, chair_actor)

    assert state.timer_is_running is True
    assert state.timer_expiration is not None


def test_delegate_cannot_toggle_timer(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    toggle_timer_event: sch.ToggleTimerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, toggle_timer_event, delegate_actor)


def test_chair_can_increase_paused_timer(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    increase_timer_event: sch.IncreaseTimerEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.timer_remaining_seconds = 30

    state = engine.dispatch(session_state, increase_timer_event, chair_actor)

    assert state.timer_remaining_seconds == 45
    assert state.timer_is_running is False


def test_delegate_cannot_increase_timer(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    increase_timer_event: sch.IncreaseTimerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, increase_timer_event, delegate_actor)


def test_chair_can_open_informal_voting(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    open_informal_voting_event: sch.OpenInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, open_informal_voting_event, chair_actor)

    assert state.current_state == enums.States.VOTING_EXECUTION
    assert state.voting is not None
    assert state.voting.target_type == enums.VotingType.INFORMAL
    assert state.voting.title == "Straw poll"
    assert state.voting.return_state == enums.States.OPEN_GSL


def test_delegate_cannot_open_informal_voting(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    open_informal_voting_event: sch.OpenInformalVotingEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, open_informal_voting_event, delegate_actor)


def test_chair_can_close_informal_voting(
    engine: eng.SessionEngine,
    informal_voting_state: md.SessionLiveState,
    close_informal_voting_event: sch.CloseInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(
        informal_voting_state, close_informal_voting_event, chair_actor
    )

    assert state.current_state == enums.States.OPEN_GSL
    assert state.voting is None


def test_chair_cannot_close_informal_voting_without_voting_context(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    close_informal_voting_event: sch.CloseInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="No voting present"):
        engine.dispatch(open_gsl_state, close_informal_voting_event, chair_actor)


def test_chair_can_resolve_motion_into_procedural_voting(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    close_speakers_list_motion: md.MotionContext,
    resolve_motion_event: sch.ResolveMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)

    state = engine.dispatch(open_gsl_state, resolve_motion_event, chair_actor)

    assert state.current_state == enums.States.VOTING_EXECUTION
    assert state.voting is not None
    assert state.voting.target_type == enums.VotingType.PROCEDURAL
    assert state.voting.motion_in_vote == close_speakers_list_motion
    assert state.submitted_motions == []


def test_chair_can_deny_motion_without_opening_vote(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    close_speakers_list_motion: md.MotionContext,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)
    event = sch.ResolveMotionEvent(
        type=enums.ChairEvents.RESOLVE_MOTION,
        payload=sch.ChairResolveMotionPayload(motion_id=1, action=False),
    )

    state = engine.dispatch(open_gsl_state, event, chair_actor)

    assert state.current_state == enums.States.OPEN_GSL
    assert state.voting is None
    assert state.submitted_motions == []


def test_delegate_cannot_resolve_motion(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    close_speakers_list_motion: md.MotionContext,
    resolve_motion_event: sch.ResolveMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)

    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, resolve_motion_event, delegate_actor)


def test_chair_can_close_passed_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: md.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    procedural_voting_state.roll_call.registry = {
        0: enums.RollCallChoice.PRESENT,
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT,
    }
    assert procedural_voting_state.voting is not None
    procedural_voting_state.voting.voting_registry = {
        0: enums.VotingChoice.FAVOUR,
        1: enums.VotingChoice.FAVOUR,
        2: enums.VotingChoice.AGAINST,
    }

    state = engine.dispatch(
        procedural_voting_state,
        close_procedural_voting_event,
        chair_actor,
    )

    assert state.current_state == enums.States.CLOSED_GSL
    assert state.voting is None


def test_chair_can_close_failed_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: md.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    procedural_voting_state.roll_call.registry = {
        0: enums.RollCallChoice.PRESENT,
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT,
    }
    assert procedural_voting_state.voting is not None
    procedural_voting_state.voting.voting_registry = {
        0: enums.VotingChoice.FAVOUR,
        1: enums.VotingChoice.AGAINST,
        2: enums.VotingChoice.AGAINST,
    }

    state = engine.dispatch(
        procedural_voting_state,
        close_procedural_voting_event,
        chair_actor,
    )

    assert state.current_state == enums.States.OPEN_GSL
    assert state.voting is None


def test_delegate_cannot_close_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: md.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(
            procedural_voting_state,
            close_procedural_voting_event,
            delegate_actor,
        )


def test_chair_can_finish_caucus_and_restore_original_gsl_state(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    finish_caucus_event: sch.FinishCaucusEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.MODERATED_CAUCUS
    open_gsl_state.current_speaker = 0
    open_gsl_state.caucus_list = [0, 1]
    open_gsl_state.timer_is_running = True
    open_gsl_state.timer_remaining_seconds = 30
    open_gsl_state.debate = md.DebateContext(
        debate_type=enums.DebateTypes.MODERATED_DEBATE,
        return_state=enums.States.OPEN_GSL,
        total_duration_seconds=600,
        per_speaker_seconds=60,
        expires_at=datetime.now(UTC),
    )

    state = engine.dispatch(open_gsl_state, finish_caucus_event, chair_actor)

    assert state.current_state == enums.States.OPEN_GSL
    assert state.debate is None
    assert state.current_speaker is None
    assert state.caucus_list == []
    assert state.timer_is_running is False
    assert state.timer_expiration is None
    assert state.timer_remaining_seconds == 0


def test_delegate_cannot_finish_caucus(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    finish_caucus_event: sch.FinishCaucusEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, finish_caucus_event, delegate_actor)


def test_chair_cannot_finish_without_active_caucus(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    finish_caucus_event: sch.FinishCaucusEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="No active caucus"):
        engine.dispatch(open_gsl_state, finish_caucus_event, chair_actor)


def test_tally_votes_correctly_marks_success_simple(
    reopen_speakers_list_motion: md.MotionContext,
) -> None:
    voting_context = md.VotingContext(
        target_type=enums.VotingType.INFORMAL,
        return_state=enums.States.OPEN_GSL,
        motion_in_vote=reopen_speakers_list_motion,
        voting_registry={
            0: enums.VotingChoice.FAVOUR,
            1: enums.VotingChoice.FAVOUR,
            2: enums.VotingChoice.FAVOUR,
            3: enums.VotingChoice.AGAINST,
            4: enums.VotingChoice.AGAINST,
        },
    )

    res = eng.tally_votes(voting_context, 5)
    assert res


def test_tally_votes_correctly_marks_fail_majority(
    close_speakers_list_motion: md.MotionContext,
) -> None:
    voting_context = md.VotingContext(
        target_type=enums.VotingType.INFORMAL,
        return_state=enums.States.OPEN_GSL,
        motion_in_vote=close_speakers_list_motion,
        voting_registry={
            0: enums.VotingChoice.FAVOUR,
            1: enums.VotingChoice.FAVOUR,
            2: enums.VotingChoice.FAVOUR,
            3: enums.VotingChoice.AGAINST,
            4: enums.VotingChoice.AGAINST,
        },
    )
    res = eng.tally_votes(voting_context, 5)
    assert not res


def test_chair_can_advance_gsl_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    next_speaker_event: sch.NextSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.gsl_queue = [1, 2]

    state = engine.dispatch(open_gsl_state, next_speaker_event, chair_actor)

    assert state.current_speaker == 1
    assert state.gsl_queue == [2]
    assert state.timer_is_running is False
    assert state.timer_expiration is None
    assert state.timer_remaining_seconds == state.gsl_default_time_seconds


def test_chair_can_advance_tour_de_table_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    next_speaker_event: sch.NextSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.TOUR_DE_TABLE
    open_gsl_state.caucus_list = [1, 2]

    state = engine.dispatch(open_gsl_state, next_speaker_event, chair_actor)

    assert state.current_speaker == 1
    assert state.caucus_list == [2]
    assert state.timer_remaining_seconds == state.gsl_default_time_seconds


def test_next_speaker_clears_current_speaker_when_gsl_empty(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    next_speaker_event: sch.NextSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_speaker = 1
    open_gsl_state.timer_is_running = True

    state = engine.dispatch(open_gsl_state, next_speaker_event, chair_actor)

    assert state.current_speaker is None
    assert state.timer_remaining_seconds == 0
    assert state.timer_is_running is False


def test_next_speaker_rejects_moderated_caucus(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    next_speaker_event: sch.NextSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.MODERATED_CAUCUS

    with pytest.raises(eng.InvalidProceduralMove, match="must grant floor"):
        engine.dispatch(open_gsl_state, next_speaker_event, chair_actor)


def test_delegate_cannot_advance_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    next_speaker_event: sch.NextSpeakerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, next_speaker_event, delegate_actor)


def test_chair_can_add_gsl_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    add_gsl_speaker_event: sch.AddGslSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, add_gsl_speaker_event, chair_actor)

    assert state.gsl_queue == [1]


def test_add_gsl_speaker_rejects_duplicates(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    add_gsl_speaker_event: sch.AddGslSpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.gsl_queue = [1]

    with pytest.raises(eng.InvalidProceduralMove, match="already in GSL queue"):
        engine.dispatch(open_gsl_state, add_gsl_speaker_event, chair_actor)


def test_chair_can_grant_floor_and_remove_gsl_queue_entry(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    grant_floor_event: sch.GrantFloorEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.gsl_queue = [0, 1, 2]

    state = engine.dispatch(open_gsl_state, grant_floor_event, chair_actor)

    assert state.current_speaker == 1
    assert state.gsl_queue == [0, 2]
    assert state.timer_remaining_seconds == 45


def test_chair_can_grant_floor_and_remove_tour_de_table_entry(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    grant_floor_event: sch.GrantFloorEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.TOUR_DE_TABLE
    open_gsl_state.caucus_list = [0, 1, 2]

    state = engine.dispatch(open_gsl_state, grant_floor_event, chair_actor)

    assert state.current_speaker == 1
    assert state.caucus_list == [0, 2]
    assert state.timer_remaining_seconds == 45


def test_chair_can_grant_floor_in_moderated_caucus(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    grant_floor_event: sch.GrantFloorEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.MODERATED_CAUCUS
    open_gsl_state.debate = md.DebateContext(
        debate_type=enums.DebateTypes.MODERATED_DEBATE,
        return_state=enums.States.OPEN_GSL,
        per_speaker_seconds=60,
    )
    open_gsl_state.caucus_list = [0, 1]

    state = engine.dispatch(open_gsl_state, grant_floor_event, chair_actor)

    assert state.current_speaker == 1
    assert state.caucus_list == [0, 1]
    assert state.timer_remaining_seconds == 45


def test_grant_floor_rejects_unmoderated_caucus(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    grant_floor_event: sch.GrantFloorEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.current_state = enums.States.UNMODERATED_CAUCUS

    with pytest.raises(eng.InvalidProceduralMove, match="unmoderated caucus"):
        engine.dispatch(open_gsl_state, grant_floor_event, chair_actor)


def test_chair_can_mark_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    mark_roll_call_event: sch.MarkRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    state = engine.dispatch(session_state, mark_roll_call_event, chair_actor)

    assert state.roll_call.registry == {1: enums.RollCallChoice.PRESENT_AND_VOTING}


@pytest.mark.anyio
def test_chair_cannot_mark_roll_call_nonexistent_delegations(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL
    event = sch.MarkRollCallEvent(
        type=enums.ChairEvents.MARK_ROLLCALL,
        payload=sch.MarkRollCallPayload(
            delegation_id=99, choice=enums.RollCallChoice.PRESENT_AND_VOTING
        ),
    )

    with pytest.raises(eng.InvalidProceduralMove):
        engine.dispatch(session_state, event, chair_actor)


def test_chair_can_mark_roll_call_bulk(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    mark_roll_call_bulk_event: sch.MarkRollCallBulkEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    state = engine.dispatch(session_state, mark_roll_call_bulk_event, chair_actor)

    assert state.roll_call.registry == {
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.ABSENT,
    }


@pytest.mark.anyio
def test_chair_cannot_mark_roll_call_bulk_nonexistent_delegations(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    roll_calls_dict = {
        1: enums.RollCallChoice.PRESENT,
        1000: enums.RollCallChoice.PRESENT_AND_VOTING,
    }

    event = sch.MarkRollCallBulkEvent(
        type=enums.ChairEvents.MARK_ROLLCALL_BULK,
        payload=sch.MarkRollCallBulkPayload(Rollcalls=roll_calls_dict),
    )

    with pytest.raises(eng.InvalidProceduralMove):
        engine.dispatch(session_state, event, chair_actor)


def test_chair_open_session_starts_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    open_session_event: sch.OpenSessionEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.SETUP
    session_state.roll_call.registry = {1: enums.RollCallChoice.PRESENT}

    state = engine.dispatch(session_state, open_session_event, chair_actor)

    assert state.current_state == enums.States.ROLL_CALL
    assert state.roll_call.registry == {}


@pytest.mark.xfail(strict=True, reason="SetAgendaEvent handler is not implemented.")
def test_chair_can_set_agenda(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    set_agenda_event: sch.SetAgendaEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, set_agenda_event, chair_actor)

    assert state.agenda_topics == [("Topic A", True), ("Topic B", True)]
    assert state.active_topic_index == 0


@pytest.mark.xfail(strict=True, reason="SetPhaseEvent handler is not implemented.")
def test_chair_can_manually_set_phase(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    manual_phase_set_event: sch.SetPhaseEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, manual_phase_set_event, chair_actor)

    assert state.current_state == enums.States.OPEN_GSL
