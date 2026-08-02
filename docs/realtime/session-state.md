# Session state

`SessionLiveState` is the server's live model of an active committee session.
The backend sends it as the initial WebSocket message and after every accepted
event. It is also persisted so an active session can be restored.

## Main fields

- **Identity:** `session_id` and `start_time` identify the session and its
  start.

- **Delegations:** `delegations` is a dictionary of delegation context keyed
  by its ID.

- **Phase:** `current_state` is the current state-machine phase, such as `Roll
  Call` or `Open GSL`.

- **Time:** `timer_is_running`, `timer_expiration`, and
  `timer_remaining_seconds` describe the session timer.

- **Speaking:** `current_speaker`, `gsl_queue`, `gsl_default_time_seconds`,
  and `debate` describe speakers and the active debate.

- **Procedure:** `submitted_motions`, `submitted_questions`, and
  `agenda_topics` hold pending procedural information.

- **Voting and attendance:** `voting`, `voting_choice`, and `roll_call` hold
  voting context and roll-call records.

## Using a snapshot on the frontend

The generated frontend type is `SessionLiveState` in
`frontend/src/schemas/types.gen.ts`. `useCommitteeStore` stores this state for
the session UI. Components should select the specific fields they display.

`delegations` is a dictionary, not an ordered list. Use an ID from a queue,
speaker field, vote, or roll call to look up its delegation directly. Use
`Object.values(delegations)` only when rendering a display list.

The state may change between a user seeing a control and sending an event. The
backend therefore remains responsible for phase and permission checks.
