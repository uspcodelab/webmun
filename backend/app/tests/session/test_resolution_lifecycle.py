import app.session.enums as enums
import app.session.models as models
import app.session.schemas as schemas


def _submit_motion(engine, state, actor, **payload):
    return engine.dispatch(
        state,
        schemas.SubmitMotionEvent(
            type=enums.DelegateEvents.SUBMIT_MOTION,
            payload=schemas.DelegateMotionPayload(**payload),
        ),
        actor,
    )


def _resolve_last(engine, state, chair):
    return engine.dispatch(
        state,
        schemas.ResolveMotionEvent(
            type=enums.ChairEvents.RESOLVE_MOTION,
            payload=schemas.ChairResolveMotionPayload(
                motion_id=state.submitted_motions[-1].id, action=True
            ),
        ),
        chair,
    )


def test_resolution_and_pending_amendment_are_voted_in_order(
    engine, session_state, delegate_actor, chair_actor
):
    session_state.current_state = enums.States.OPEN_GSL
    _resolve_last(
        engine,
        _submit_motion(
            engine,
            session_state,
            delegate_actor,
            type=enums.Motions.INTRODUCE_RESOLUTION_PROPOSAL,
            resolution_title="Clean Water",
            resolution_id="resolution-clean-water",
        ),
        chair_actor,
    )
    resolution = session_state.draft_resolutions[0]
    _resolve_last(
        engine,
        _submit_motion(
            engine,
            session_state,
            delegate_actor,
            type=enums.Motions.INTRODUCE_AMENDMENT_PROPOSAL,
            target_resolution_id=resolution.id,
            amendment_id="amendment-clean-water-1",
            is_friendly=False,
        ),
        chair_actor,
    )

    session_state.current_state = enums.States.VOTING_PREPARATION
    engine.dispatch(
        session_state,
        schemas.StartResolutionVoteEvent(
            type=enums.ChairEvents.START_RESOLUTION_VOTE,
            payload=schemas.EmptyPayload(),
        ),
        chair_actor,
    )
    assert session_state.voting is not None
    assert session_state.voting.amendment_in_vote is not None

    session_state.roll_call.registry = {0: enums.RollCallChoice.PRESENT}
    engine.dispatch(
        session_state,
        schemas.CastVoteEvent(
            type=enums.DelegateEvents.CAST_VOTE,
            payload=schemas.DelegateVotingPayload(vote=enums.VotingChoice.FAVOUR),
        ),
        delegate_actor,
    )
    engine.dispatch(
        session_state,
        schemas.CloseProceduralVotingEvent(
            type=enums.ChairEvents.CLOSE_PROCEDURAL_VOTING,
            payload=schemas.EmptyPayload(),
        ),
        chair_actor,
    )
    assert resolution.amendments[0].status == enums.AmendmentStatus.ADOPTED
    assert session_state.voting is not None
    assert session_state.voting.target_type == enums.VotingType.SUBSTANTIVE


def test_roll_call_requires_all_votes_then_processes_rights_queue(
    engine, session_state, chair_actor
):
    resolution = models.ResolutionContext(
        id="resolution-1", title="Test", delegate_id=0, roll_call_vote=True
    )
    session_state.draft_resolutions.append(resolution)
    session_state.current_state = enums.States.VOTING_PREPARATION
    session_state.roll_call.registry = {
        0: enums.RollCallChoice.PRESENT,
        1: enums.RollCallChoice.PRESENT_AND_VOTING,
    }
    engine.dispatch(
        session_state,
        schemas.StartResolutionVoteEvent(
            type=enums.ChairEvents.START_RESOLUTION_VOTE,
            payload=schemas.EmptyPayload(),
        ),
        chair_actor,
    )
    for representation_id, vote in (
        (0, enums.VotingChoice.YES_WITH_RIGHTS),
        (1, enums.VotingChoice.AGAINST),
    ):
        engine.dispatch(
            session_state,
            schemas.RecordSubstantiveVoteEvent(
                type=enums.ChairEvents.RECORD_SUBSTANTIVE_VOTE,
                payload=schemas.RecordSubstantiveVotePayload(
                    representation_id=representation_id, vote=vote
                ),
            ),
            chair_actor,
        )
    advance = schemas.AdvanceSubstantiveVoteRoundEvent(
        type=enums.ChairEvents.ADVANCE_SUBSTANTIVE_VOTE_ROUND,
        payload=schemas.EmptyPayload(),
    )
    engine.dispatch(session_state, advance, chair_actor)
    assert session_state.voting is not None
    assert session_state.voting.rights_queue == [0]
    engine.dispatch(
        session_state,
        schemas.NextSpeakerEvent(
            type=enums.ChairEvents.NEXT_SPEAKER, payload=schemas.EmptyPayload()
        ),
        chair_actor,
    )
    assert session_state.timer_remaining_seconds == 30
    engine.dispatch(session_state, advance, chair_actor)
    engine.dispatch(session_state, advance, chair_actor)
    assert resolution.status == enums.ResolutionStatus.ADOPTED
    assert session_state.current_state == enums.States.VOTING_PREPARATION
