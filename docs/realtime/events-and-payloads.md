# Events and payloads

This page lists the event messages currently accepted by the session WebSocket.
The backend schema is the source of truth; frontend types are generated in `frontend/src/schemas/types.gen.ts` with `npm run generate:schema`.

An event is an action a client requests. Its payload is the event-specific input. The backend obtains the caller's identity from the WebSocket token and validates the event against the current session state.

## Quick rules

- Send the exact `type` string shown below.
- Send `{}` when the payload is empty.
- Use the generated TypeScript event and payload types; do not duplicate them.
- Wait for the next server snapshot instead of modifying shared session state locally.
- An ID that targets a delegation must refer to one in `state.delegations`.

## Delegate events

- `SubmitMotionEvent`
  - Payload: `type`, `delegate`, and optional `debate_type`,
    `total_duration_minutes`, `per_speaker_seconds`, `target_topic`, and
    `details`.
  - Submits a motion allowed in the current phase. The backend records the
    submitting delegate from the authenticated actor.

- `SubmitQuestionEvent`
  - Payload: `type`, `delegate`, and optional `details`.
  - Submits a delegate question and adds it to the pending questions.

- `JoinQueueEvent`
  - Payload: `{}`.
  - Adds the authenticated delegate to the open GSL queue.

- `LeaveQueueEvent`
  - Payload: `{}`.
  - Removes the authenticated delegate from the open GSL queue.

- `CastVoteEvent`
  - Payload: `type` (`FORMAL` or `INFORMAL`), `vote` (`FAVOUR`, `AGAINST`, or
    `ABSTAIN`), and optional `motion_id` and `title`.
  - Records one vote from the authenticated delegate while voting is active.

- `AnswerRollCallEvent`
  - Payload: `choice` (`Present` or `Present and Voting`).
  - Records the authenticated delegate's roll-call response.

- `ChooseDelegateEvent`
  - Payload: `choice`.
  - Declared in the schema, but its handler is not implemented. Do not use it
    yet.

### Motion payload values

`SubmitMotionEvent.payload.type` is one of the backend `Motions` values, such
as `Mudar Tipo de Debate`, `Encerramento de Debate`, or `Quórum`. Which motion types are allowed depends on `current_state`. The optional fields are validated when the selected motion needs them; for example, a debate-type motion can need `debate_type` and duration information.

### Question payload values

`SubmitQuestionEvent.payload.type` is `Order`, `Question`, or `Personal
Privilege`.

## Chair events

- `OpenSessionEvent`
  - Payload: `{}`.
  - Moves a session from setup to roll call and resets live procedure fields.

- `CloseSessionEvent`
  - Payload: `{}`.
  - Moves an allowed session to `Finished` and clears active debate and timer
    data.

- `ToggleTimerEvent`
  - Payload: optional `toggle` (defaults to `true`).
  - Starts or pauses the timer. The current implementation toggles based on
    timer state.

- `IncreaseTimerEvent`
  - Payload: optional `seconds` (defaults to `5`).
  - Adds seconds to the running or paused timer.

- `OpenInformalVotingEvent`
  - Payload: optional `title`; required `majority` (`SIMPLE`, `QUALIFIED`, or
    `ABSOLUTE`) and `veto_power`.
  - Opens an informal vote and changes the session to voting execution.

- `CloseInformalVotingEvent`
  - Payload: optional `voting_id`.
  - Closes the current informal vote and returns to the previous phase.

- `ResolveMotionEvent`
  - Payload: `motion_id` and `action` (`ACCEPT` or `DENY`).
  - Removes a submitted motion; accepting it opens procedural voting for that
    motion.

- `CloseProceduralVotingEvent`
  - Payload: `{}`.
  - Tallies the current procedural vote and applies its result or returns to
    the earlier phase.

- `SpeakerEvent`
  - Payload: optional `speaker_id` and `seconds`.
  - Sets a current speaker and the timer duration. Although the schema allows
    an omitted `speaker_id`, the current handler requires an existing
    delegation ID.

- `MarkRollCallEvent`
  - Payload: `delegation_id` and `choice` (`Present`, `Present and Voting`, or
    `Absent`).
  - Sets one delegation's roll-call status during roll call.

- `Mark Roll Call Bulk Event`
  - Payload: `Rollcalls`, a delegation-ID-to-choice map.
  - Sets multiple roll-call statuses during roll call. All referenced
    delegations must exist.

- `CloseRollCallEvent`
  - Payload: `{}`.
  - Marks unrecorded delegations absent, creates voting eligibility, and moves
    to Open GSL.

- `InsertQueueEvent`
  - Payload: `target`.
  - Adds the target delegation to the GSL queue.

- `SetAgendaEvent`
  - Payload: `agenda`, a list of strings.
  - Declared in the schema, but its handler is not implemented. Do not use it
    yet.

- `SetPhaseEvent`
  - Payload: `target_phase`, a session-state value.
  - Declared in the schema, but its handler is not implemented. Do not use it
    yet.

## Example

A chair marking a delegation present sends:

```json
{
  "type": "MarkRollCallEvent",
  "payload": {
    "delegation_id": 42,
    "choice": "Present"
  }
}
```

The backend checks that the caller is a chair, roll call is open, and delegation `42` is in the session. It then broadcasts the updated `SessionLiveState`.

## Not yet part of the WebSocket protocol

TODO: some pieces of events are not yet used.
