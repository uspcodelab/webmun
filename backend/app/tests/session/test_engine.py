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
def voting_state(session_state: md.SessionLiveState) -> md.SessionLiveState:
    session_state.current_state = enums.States.VOTING_EXECUTION
    session_state.voting = md.VotingContext(
        target_type="INFORMAL",
        return_state=enums.States.OPEN_GSL,
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
        type=enums.DelegateEvents.SUBMIT_MOTION,
        payload=sch.DelegateMotionPayload(
            type=enums.Motions.CHANGE_DEBATE_TYPE,
            delegate=delegate_actor.delegation.id,  # type: ignore[union-attr]
            debate_type=enums.DebateTypes.MODERATED_DEBATE,
            total_duration_minutes=10,
            per_speaker_seconds=60,
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
        payload=sch.DelegateVotingPayload(type="FORMAL", vote="FAVOUR"),
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
            majority="SIMPLE",
            veto_power=False,
        ),
    )


@pytest.fixture
def close_informal_voting_event() -> sch.CloseInformalVotingEvent:
    return sch.CloseInformalVotingEvent(
        type=enums.ChairEvents.CLOSE_INFORMAL_VOTING,
        payload=sch.ChairCloseInformalVotingPayload(),
    )


@pytest.fixture
def close_procedural_voting_event() -> sch.CloseProceduralVotingEvent:
    return sch.CloseProceduralVotingEvent(
        type=enums.ChairEvents.CLOSE_PROCEDURAL_VOTING,
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
        delegate_id=delegate_actor.delegation.id,  # type: ignore[union-attr]
    )


@pytest.fixture
def procedural_voting_state(
    open_gsl_state: md.SessionLiveState,
    close_speakers_list_motion: md.MotionContext,
) -> md.SessionLiveState:
    open_gsl_state.current_state = enums.States.VOTING_EXECUTION
    open_gsl_state.voting = md.VotingContext(
        target_type="PROCEDURAL",
        motion_in_vote=close_speakers_list_motion,
        return_state=enums.States.OPEN_GSL,
        voting_registry={},
        majority="SIMPLE",
        veto_power=False,
    )
    return open_gsl_state


@pytest.fixture
def resolve_motion_event() -> sch.ResolveMotionEvent:
    return sch.ResolveMotionEvent(
        type=enums.ChairEvents.RESOLVE_MOTION,
        payload=sch.ChairResolveMotionPayload(motion_id=1, action="ACCEPT"),
    )


@pytest.fixture
def choose_speaker_event() -> sch.SpeakerEvent:
    return sch.SpeakerEvent(
        type=enums.ChairEvents.CHOOSE_SPEAKER,
        payload=sch.ChairForceSpeakerPayload(speaker_id=1, seconds=45),
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
def insert_queue_event() -> sch.ChairInsertQueueEvent:
    return sch.ChairInsertQueueEvent(
        type=enums.ChairEvents.INSERT_QUEUE,
        payload=sch.ChairInsertQueuePayload(target=0),
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


@pytest.mark.xfail(strict=True, reason="get_motion_priority is not implemented.")
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
    assert state.submitted_motions[0].delegate_id == 1


def test_delegate_cannot_submit_motion_outside_allowed_phase(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Cannot submit this motion"):
        engine.dispatch(session_state, submit_debate_motion_event, delegate_actor)


@pytest.mark.xfail(
    strict=True,
    reason="handle_submit_motion does not currently reject chair actors.",
)
def test_chair_cannot_submit_delegate_motion(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    submit_debate_motion_event: sch.SubmitMotionEvent,
    chair_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Delegate role required"):
        engine.dispatch(open_gsl_state, submit_debate_motion_event, chair_actor)


@pytest.mark.xfail(strict=True, reason="get_question_priority is not implemented.")
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
    assert state.submitted_questions[0].delegate_id == 1


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
    voting_state: md.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(voting_state, cast_vote_event, delegate_actor)

    assert state.voting is not None
    assert state.voting.voting_registry == {0: "FAVOUR"}


def test_delegate_cannot_cast_vote_twice(
    engine: eng.SessionEngine,
    voting_state: md.SessionLiveState,
    cast_vote_event: sch.CastVoteEvent,
    delegate_actor: md.SessionActor,
) -> None:
    engine.dispatch(voting_state, cast_vote_event, delegate_actor)

    with pytest.raises(eng.InvalidProceduralMove, match="Already cast vote"):
        engine.dispatch(voting_state, cast_vote_event, delegate_actor)


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
    assert state.voting_choice == {
        1: enums.RollCallChoice.PRESENT,
        2: enums.RollCallChoice.PRESENT_AND_VOTING,
    }


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
    assert state.voting.target_type == "INFORMAL"
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
    voting_state: md.SessionLiveState,
    close_informal_voting_event: sch.CloseInformalVotingEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(voting_state, close_informal_voting_event, chair_actor)

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
    assert state.voting.target_type == "PROCEDURAL"
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
        payload=sch.ChairResolveMotionPayload(motion_id=1, action="DENY"),
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(eng, "tally_votes", lambda voting: True)

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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(eng, "tally_votes", lambda voting: False)

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


def test_chair_can_choose_speaker(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
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
    open_gsl_state: md.SessionLiveState,
    choose_speaker_event: sch.SpeakerEvent,
    delegate_actor: md.SessionActor,
) -> None:
    with pytest.raises(eng.InvalidProceduralMove, match="Chair role required"):
        engine.dispatch(open_gsl_state, choose_speaker_event, delegate_actor)


def test_chair_can_mark_roll_call(
    engine: eng.SessionEngine,
    session_state: md.SessionLiveState,
    mark_roll_call_event: sch.MarkRollCallEvent,
    chair_actor: md.SessionActor,
) -> None:
    session_state.current_state = enums.States.ROLL_CALL

    state = engine.dispatch(session_state, mark_roll_call_event, chair_actor)

    assert state.roll_call.registry == {1: enums.RollCallChoice.PRESENT_AND_VOTING}


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


# @pytest.mark.xfail(
#    strict=True,
#    reason="handle_insert_queue currently treats delegation id as list index.",
# )
def test_chair_insert_queue_uses_delegation_id(
    engine: eng.SessionEngine,
    open_gsl_state: md.SessionLiveState,
    insert_queue_event: sch.ChairInsertQueueEvent,
    chair_actor: md.SessionActor,
) -> None:
    state = engine.dispatch(open_gsl_state, insert_queue_event, chair_actor)

    assert state.gsl_queue == [0]


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
