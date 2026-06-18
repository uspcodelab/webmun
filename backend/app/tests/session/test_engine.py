import pytest

import app.session.engine as eng
import app.session.manager as man
import app.session.models as md
import app.session.schemas as sch


@pytest.fixture
def open_gsl_state(session_state: man.SessionLiveState) -> man.SessionLiveState:
    session_state.current_state = sch.States.OPEN_GSL
    return session_state


@pytest.fixture
def voting_state(session_state: man.SessionLiveState) -> man.SessionLiveState:
    session_state.current_state = sch.States.VOTING_EXECUTION
    session_state.voting = man.VotingContext(
        target_type="INFORMAL",
        return_state=sch.States.OPEN_GSL,
        voting_registry={},
        majority="SIMPLE",
        veto_power=False,
    )
    return session_state


@pytest.fixture
def submit_debate_motion_event(
    delegate_actor: md.SessionActor,
) -> sch.SubmitMotionEvent:
    return sch.SubmitMotionEvent(
        type=sch.DelegateEvents.SUBMIT_MOTION,
        payload=sch.DelegateMotionPayload(
            priority=1,
            type=sch.Motions.CHANGE_DEBATE_TYPE,
            delegate=delegate_actor.delegation,  # type: ignore[arg-type]
            debate_type=sch.DebateTypes.MODERATED_DEBATE,
            total_duration_minutes=10,
            per_speaker_seconds=60,
        ),
    )


@pytest.fixture
def submit_question_event(delegate_actor: md.SessionActor) -> sch.SubmitQuestionEvent:
    return sch.SubmitQuestionEvent(
        type=sch.DelegateEvents.SUBMIT_QUESTION,
        payload=sch.DelegateQuestionPayload(
            priority=0,
            type=sch.Questions.PERSONAL_PRIVILEGE,
            delegate=delegate_actor.delegation,  # type: ignore[arg-type]
            details="Need technical assistance.",
        ),
    )


@pytest.fixture
def join_queue_event() -> sch.JoinQueueEvent:
    return sch.JoinQueueEvent(type=sch.DelegateEvents.JOIN_QUEUE, payload={})


@pytest.fixture
def leave_queue_event() -> sch.LeaveQueueEvent:
    return sch.LeaveQueueEvent(type=sch.DelegateEvents.LEAVE_QUEUE, payload={})


@pytest.fixture
def cast_vote_event() -> sch.CastVoteEvent:
    return sch.CastVoteEvent(
        type=sch.DelegateEvents.CAST_VOTE,
        payload=sch.DelegateVotingPayload(type="FORMAL", vote="FAVOUR"),
    )


@pytest.fixture
def answer_roll_call_event() -> sch.AnswerRollCallEvent:
    return sch.AnswerRollCallEvent(
        type=sch.DelegateEvents.ANSWER_ROLLCALL,
        payload=sch.AnswerRollCallPayload(choice=sch.RollCallChoice.PRESENT),
    )


@pytest.fixture
def close_roll_call_event() -> sch.CloseRollCallEvent:
    return sch.CloseRollCallEvent(
        type=sch.ChairEvents.CLOSE_ROLLCALL,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def toggle_timer_event() -> sch.ToggleTimerEvent:
    return sch.ToggleTimerEvent(
        type=sch.ChairEvents.TOGGLE_TIMER,
        payload=sch.ChairToggleTimerPayload(toggle=True),
    )


def test_delegate_can_submit_motion_in_open_gsl(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, submit_debate_motion_event, delegate_actor)

    assert len(state.submitted_motions) == 1
    assert state.submitted_motions[0].id == 1
    assert state.submitted_motions[0].type == sch.Motions.CHANGE_DEBATE_TYPE
    assert state.submitted_motions[0].delegate.name == "Brazil"


def test_delegate_cannot_submit_motion_outside_allowed_phase(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot submit this motion"):
        engine.dispatch(session_state, submit_debate_motion_event, delegate_actor)


def test_chair_cannot_submit_delegate_motion(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Delegate role required"):
        engine.dispatch(open_gsl_state, submit_debate_motion_event, chair_actor)


def test_delegate_can_submit_question(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    submit_question_event: sch.SubmitQuestionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, submit_question_event, delegate_actor)

    assert len(state.submitted_questions) == 1
    assert state.submitted_questions[0].id == 1
    assert state.submitted_questions[0].type == sch.Questions.PERSONAL_PRIVILEGE
    assert state.submitted_questions[0].delegate.name == "Brazil"


def test_delegate_can_join_queue(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)

    assert state.gsl_queue == [1]


def test_delegate_cannot_join_queue_twice(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)

    with pytest.raises(eng.InvalidProceduralMove, match="Already in Queue"):
        engine.dispatch(open_gsl_state, join_queue_event, delegate_actor)


def test_delegate_cannot_join_queue_outside_open_gsl(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot enter queue"):
        engine.dispatch(session_state, join_queue_event, delegate_actor)


def test_chair_cannot_join_queue(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    join_queue_event: sch.JoinQueueEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Delegate role required"):
        engine.dispatch(open_gsl_state, join_queue_event, chair_actor)


def test_delegate_can_leave_queue(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    leave_queue_event: sch.LeaveQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    open_gsl_state.gsl_queue.append(1)

    state = engine.dispatch(open_gsl_state, leave_queue_event, delegate_actor)

    assert state.gsl_queue == []


def test_delegate_cannot_leave_queue_when_not_queued(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    leave_queue_event: sch.LeaveQueueEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Not in Queue"):
        engine.dispatch(open_gsl_state, leave_queue_event, delegate_actor)


def test_delegate_can_cast_vote(
    engine: eng.SessionEngine,
    voting_state: man.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(voting_state, cast_vote_event, delegate_actor)

    assert state.voting is not None
    assert state.voting.voting_registry == {1: "FAVOUR"}


def test_delegate_cannot_cast_vote_twice(
    engine: eng.SessionEngine,
    voting_state: man.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    engine.dispatch(voting_state, cast_vote_event, delegate_actor)

    with pytest.raises(eng.InvalidProceduralMove, match="Already cast vote"):
        engine.dispatch(voting_state, cast_vote_event, delegate_actor)


def test_delegate_cannot_cast_vote_without_voting_context(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot vote"):
        engine.dispatch(session_state, cast_vote_event, delegate_actor)


def test_delegate_can_answer_roll_call(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    answer_roll_call_event: sch.AnswerRollCallEvent,
    delegate_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.ROLL_CALL

    state = engine.dispatch(session_state, answer_roll_call_event, delegate_actor)

    assert state.roll_call.registry == {1: sch.RollCallChoice.PRESENT}


def test_chair_can_close_roll_call(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    close_roll_call_event: sch.CloseRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.ROLL_CALL
    session_state.roll_call.registry = {
        1: sch.RollCallChoice.PRESENT,
        2: sch.RollCallChoice.PRESENT_AND_VOTING,
        3: sch.RollCallChoice.ABSENT,
    }

    state = engine.dispatch(session_state, close_roll_call_event, chair_actor)

    assert state.current_state == sch.States.OPEN_GSL
    assert state.voting_choice == {
        1: sch.RollCallChoice.PRESENT,
        2: sch.RollCallChoice.PRESENT_AND_VOTING,
    }


def test_delegate_cannot_close_roll_call(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    close_roll_call_event: sch.CloseRollCallEvent,
    delegate_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.ROLL_CALL

    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, close_roll_call_event, delegate_actor)


def test_chair_can_toggle_timer(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    toggle_timer_event: sch.ToggleTimerEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.timer_remaining_seconds = 30

    state = engine.dispatch(session_state, toggle_timer_event, chair_actor)

    assert state.timer_is_running is True
    assert state.timer_expiration is not None


def test_delegate_cannot_toggle_timer(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    toggle_timer_event: sch.ToggleTimerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, toggle_timer_event, delegate_actor)
