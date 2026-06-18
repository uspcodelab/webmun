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


@pytest.fixture
def increase_timer_event() -> sch.IncreaseTimerEvent:
    return sch.IncreaseTimerEvent(
        type=sch.ChairEvents.INCREASE_TIMER,
        payload=sch.ChairIncreaseTimerPayload(seconds=15),
    )


@pytest.fixture
def open_informal_voting_event() -> sch.OpenInformalVotingEvent:
    return sch.OpenInformalVotingEvent(
        type=sch.ChairEvents.OPEN_INFORMAL_VOTING,
        payload=sch.ChairOpenInformalVotingPayload(
            title="Straw poll",
            majority="SIMPLE",
            veto_power=False,
        ),
    )


@pytest.fixture
def close_informal_voting_event() -> sch.CloseInformalVotingEvent:
    return sch.CloseInformalVotingEvent(
        type=sch.ChairEvents.CLOSE_INFORMAL_VOTING,
        payload=sch.ChairCloseInformalVotingPayload(),
    )


@pytest.fixture
def close_procedural_voting_event() -> sch.CloseProceduralVotingEvent:
    return sch.CloseProceduralVotingEvent(
        type=sch.ChairEvents.CLOSE_PROCEDURAL_VOTING,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def close_speakers_list_motion(
    delegate_actor: md.SessionActor,
) -> sch.DelegateMotionPayload:
    return sch.DelegateMotionPayload(
        id=1,
        priority=1,
        type=sch.Motions.CLOSE_SPEAKERS_LIST,
        delegate=delegate_actor.delegation,  # type: ignore[arg-type]
    )


@pytest.fixture
def procedural_voting_state(
    open_gsl_state: man.SessionLiveState,
    close_speakers_list_motion: sch.DelegateMotionPayload,
) -> man.SessionLiveState:
    open_gsl_state.current_state = sch.States.VOTING_EXECUTION
    open_gsl_state.voting = man.VotingContext(
        target_type="PROCEDURAL",
        motion_in_vote=close_speakers_list_motion,
        return_state=sch.States.OPEN_GSL,
        voting_registry={},
        majority="SIMPLE",
        veto_power=False,
    )
    return open_gsl_state


@pytest.fixture
def resolve_motion_event() -> sch.ResolveMotionEvent:
    return sch.ResolveMotionEvent(
        type=sch.ChairEvents.RESOLVE_MOTION,
        payload=sch.ChairResolveMotionPayload(motion_id=1, action="ACCEPT"),
    )


@pytest.fixture
def choose_speaker_event() -> sch.SpeakerEvent:
    return sch.SpeakerEvent(
        type=sch.ChairEvents.CHOOSE_SPEAKER,
        payload=sch.ChairForceSpeakerPayload(speaker_id=1, seconds=45),
    )


@pytest.fixture
def mark_roll_call_event() -> sch.MarkRollCallEvent:
    return sch.MarkRollCallEvent(
        type=sch.ChairEvents.MARK_ROLLCALL,
        payload=sch.MarkRollCallPayload(
            delegation_id=1,
            choice=sch.RollCallChoice.PRESENT_AND_VOTING,
        ),
    )


@pytest.fixture
def mark_roll_call_bulk_event() -> sch.MarkRollCallBulkEvent:
    return sch.MarkRollCallBulkEvent(
        type=sch.ChairEvents.MARK_ROLLCALL_BULK,
        payload=sch.MarkRollCallBulkPayload(
            Rollcalls={
                1: sch.RollCallChoice.PRESENT,
                2: sch.RollCallChoice.ABSENT,
            },
        ),
    )


@pytest.fixture
def insert_queue_event() -> sch.ChairInsertQueueEvent:
    return sch.ChairInsertQueueEvent(
        type=sch.ChairEvents.INSERT_QUEUE,
        payload=sch.ChairInsertQueuePayload(target=1),
    )


@pytest.fixture
def open_session_event() -> sch.OpenSessionEvent:
    return sch.OpenSessionEvent(
        type=sch.ChairEvents.OPEN_SESSION,
        payload=sch.EmptyPayload(),
    )


@pytest.fixture
def set_agenda_event() -> sch.SetAgendaEvent:
    return sch.SetAgendaEvent(
        type=sch.ChairEvents.SET_AGENDA,
        payload=sch.ChairSetAgendaPayload(agenda=["Topic A", "Topic B"]),
    )


@pytest.fixture
def manual_phase_set_event() -> sch.SetPhaseEvent:
    return sch.SetPhaseEvent(
        type=sch.ChairEvents.MANUAL_PHASE_SET,
        payload=sch.ChairSetPhasePayload(target_phase=sch.States.OPEN_GSL),
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


def test_chair_can_increase_paused_timer(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    increase_timer_event: sch.IncreaseTimerEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.timer_remaining_seconds = 30

    state = engine.dispatch(session_state, increase_timer_event, chair_actor)

    assert state.timer_remaining_seconds == 45
    assert state.timer_is_running is False


def test_delegate_cannot_increase_timer(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    increase_timer_event: sch.IncreaseTimerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(session_state, increase_timer_event, delegate_actor)


def test_chair_can_open_informal_voting(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    open_informal_voting_event: sch.OpenInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, open_informal_voting_event, chair_actor)

    assert state.current_state == sch.States.VOTING_EXECUTION
    assert state.voting is not None
    assert state.voting.target_type == "INFORMAL"
    assert state.voting.title == "Straw poll"
    assert state.voting.return_state == sch.States.OPEN_GSL


def test_delegate_cannot_open_informal_voting(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    open_informal_voting_event: sch.OpenInformalVotingEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, open_informal_voting_event, delegate_actor)


def test_chair_can_close_informal_voting(
    engine: eng.SessionEngine,
    voting_state: man.SessionLiveState,
    close_informal_voting_event: sch.CloseInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(voting_state, close_informal_voting_event, chair_actor)

    assert state.current_state == sch.States.OPEN_GSL
    assert state.voting is None


def test_chair_cannot_close_informal_voting_without_voting_context(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    close_informal_voting_event: sch.CloseInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="No voting present"):
        engine.dispatch(open_gsl_state, close_informal_voting_event, chair_actor)


def test_chair_can_resolve_motion_into_procedural_voting(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    close_speakers_list_motion: sch.DelegateMotionPayload,
    resolve_motion_event: sch.ResolveMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)

    state = engine.dispatch(open_gsl_state, resolve_motion_event, chair_actor)

    assert state.current_state == sch.States.VOTING_EXECUTION
    assert state.voting is not None
    assert state.voting.target_type == "PROCEDURAL"
    assert state.voting.motion_in_vote == close_speakers_list_motion
    assert state.submitted_motions == []


def test_chair_can_deny_motion_without_opening_vote(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    close_speakers_list_motion: sch.DelegateMotionPayload,
    chair_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)
    event = sch.ResolveMotionEvent(
        type=sch.ChairEvents.RESOLVE_MOTION,
        payload=sch.ChairResolveMotionPayload(motion_id=1, action="DENY"),
    )

    state = engine.dispatch(open_gsl_state, event, chair_actor)

    assert state.current_state == sch.States.OPEN_GSL
    assert state.voting is None
    assert state.submitted_motions == []


def test_delegate_cannot_resolve_motion(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    close_speakers_list_motion: sch.DelegateMotionPayload,
    resolve_motion_event: sch.ResolveMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    open_gsl_state.submitted_motions.append(close_speakers_list_motion)

    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, resolve_motion_event, delegate_actor)


def test_chair_can_close_passed_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: man.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    chair_actor: md.SessionActor,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(eng, "tally_votes", lambda voting: True)

    state = engine.dispatch(
        procedural_voting_state,
        close_procedural_voting_event,
        chair_actor,
    )

    assert state.current_state == sch.States.CLOSED_GSL
    assert state.voting is None


def test_chair_can_close_failed_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: man.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    chair_actor: md.SessionActor,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(eng, "tally_votes", lambda voting: False)

    state = engine.dispatch(
        procedural_voting_state,
        close_procedural_voting_event,
        chair_actor,
    )

    assert state.current_state == sch.States.OPEN_GSL
    assert state.voting is None


def test_delegate_cannot_close_procedural_vote(
    engine: eng.SessionEngine,
    procedural_voting_state: man.SessionLiveState,
    close_procedural_voting_event: sch.CloseProceduralVotingEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(
            procedural_voting_state,
            close_procedural_voting_event,
            delegate_actor,
        )


def test_chair_can_choose_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    choose_speaker_event: sch.SpeakerEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, choose_speaker_event, chair_actor)

    assert state.current_speaker == 1
    assert state.timer_is_running is False
    assert state.timer_expiration is None
    assert state.timer_remaining_seconds == 45


def test_delegate_cannot_choose_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    choose_speaker_event: sch.SpeakerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, choose_speaker_event, delegate_actor)


def test_chair_can_mark_roll_call(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    mark_roll_call_event: sch.MarkRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.ROLL_CALL

    state = engine.dispatch(session_state, mark_roll_call_event, chair_actor)

    assert state.roll_call.registry == {1: sch.RollCallChoice.PRESENT_AND_VOTING}


def test_chair_can_mark_roll_call_bulk(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    mark_roll_call_bulk_event: sch.MarkRollCallBulkEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.ROLL_CALL

    state = engine.dispatch(session_state, mark_roll_call_bulk_event, chair_actor)

    assert state.roll_call.registry == {
        1: sch.RollCallChoice.PRESENT,
        2: sch.RollCallChoice.ABSENT,
    }


@pytest.mark.xfail(
    strict=True,
    reason="handle_insert_queue currently treats delegation id as list index.",
)
def test_chair_insert_queue_uses_delegation_id(
    engine: eng.SessionEngine,
    open_gsl_state: man.SessionLiveState,
    insert_queue_event: sch.ChairInsertQueueEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, insert_queue_event, chair_actor)

    assert state.gsl_queue == [1]


@pytest.mark.xfail(strict=True, reason="OpenSessionEvent handler is not implemented.")
def test_chair_open_session_starts_roll_call(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    open_session_event: sch.OpenSessionEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = sch.States.SETUP
    session_state.roll_call.registry = {1: sch.RollCallChoice.PRESENT}

    state = engine.dispatch(session_state, open_session_event, chair_actor)

    assert state.current_state == sch.States.ROLL_CALL
    assert state.roll_call.registry == {}


@pytest.mark.xfail(strict=True, reason="SetAgendaEvent handler is not implemented.")
def test_chair_can_set_agenda(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    set_agenda_event: sch.SetAgendaEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, set_agenda_event, chair_actor)

    assert state.agenda_topics == [("Topic A", True), ("Topic B", True)]
    assert state.active_topic_index == 0


@pytest.mark.xfail(strict=True, reason="SetPhaseEvent handler is not implemented.")
def test_chair_can_manually_set_phase(
    engine: eng.SessionEngine,
    session_state: man.SessionLiveState,
    manual_phase_set_event: sch.SetPhaseEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(session_state, manual_phase_set_event, chair_actor)

    assert state.current_state == sch.States.OPEN_GSL
