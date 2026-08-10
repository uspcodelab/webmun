# MUN committee flow and technical approach

This page describes the top-level flow of a typical Model United Nations
(MUN) committee and how WebMUN represents it. It is a product and engineering
guide: conference rules of procedure vary, so the chair remains responsible
for applying the committee's adopted rules.

The backend is the source of truth. A user interface may guide a delegate or
chair toward actions that make sense in the displayed phase, but only the
backend can accept an action and move the committee forward.

## Committee flow at a glance

```text
Setup Room
   |
   | chair opens the session
   v
Roll Call
   |
   | chair closes roll call and establishes attendance/voting eligibility
   v
Open GSL <-------------------------------+
   |                                     |
   | delegates join the speakers list    | informal vote closes
   | chair selects speakers              |
   |                                     |
   +-- procedural motion --> Voting Execution
   |                            |          |
   |                            | passed   | denied
   |                            v          |
   |                   Open/Closed GSL,    |
   |                   caucus, roll call,  |
   |                   or voting procedures|
   |                                       |
   +-- chair opens informal vote ----------+
   |
   +-- accepted debate-type motion --> Moderated/Unmoderated Caucus
                                          |
                                          | next implemented transition
                                          v
                                      procedural motion / chair action

Open or Closed GSL -- accepted end-debate motion --> Voting Preparation
                                                        |
                                                        | chair starts next draft
                                                        v
                                                   Voting Procedures
                                                        |
                                   pending amendments -> procedural amendment votes
                                                        |
                                                        v
                                             substantive resolution vote
                                                        |
                                                        v
                                                 Voting Preparation
```

`Finished` can also be reached when the chair closes the session from an
allowed phase. The diagram is deliberately a workflow view, not a complete
transition table: an informal vote can be opened by the chair from any phase
other than `Voting Execution`, and returns to the phase from which it opened.

## Typical procedure, mapped to WebMUN

### 1. Prepare the session

Before formal business, durable conference data identifies the committee,
participants, and chair assignments. Starting a live session creates a
`SessionLiveState` in `Setup Room`. This live state contains the delegations,
agenda context, timer, queues, roll call, motions, and voting information used
while the committee is active.

The chair sends `OpenSessionEvent` to move the session to `Roll Call`.

### 2. Take roll call and establish quorum

During `Roll Call`, the chair can mark a representation as `Present`,
`Present and Voting`, or `Absent`. A delegate may report their own presence
with `AnswerRollCallEvent`; the chair remains able to correct the record.

When the chair sends `CloseRollCallEvent`, any unrecorded representation is
marked absent. WebMUN then derives `voting_choice` from the recorded present
representations and moves to `Open GSL`. The identity used here and throughout
the flow is `representation_id`, never a client-asserted country or delegate
identity.

### 3. Conduct general debate

`Open GSL` is the normal working phase. Delegates may join or leave the
General Speakers List (GSL); the chair can insert a representation or select
the next speaker. Speaker selection sets the timer; timer controls are chair
actions. Delegates can submit motions and questions for chair consideration.

The chair may accept or deny a submitted motion. Accepting it opens a
procedural vote in `Voting Execution`; denying it removes it without changing
the phase. A failed procedural vote returns to the earlier phase.

An accepted motion can currently produce these transitions:

- change debate type to a moderated or unmoderated caucus;
- close or reopen the GSL;
- reopen roll call to check quorum; or
- end debate and enter `Voting Procedures`.

Some defined motion types are not yet given a concrete effect by the engine.
They must not be presented as a completed procedure until their transition and
data model are implemented.

### 4. Run caucuses

A moderated caucus has an overall debate duration and an individual speaking
time. A chair chooses speakers; the GSL queue is not used for the automatic
order. An unmoderated caucus has an overall duration but no individual speaker
timer.

The current engine does not automatically advance when a caucus duration
expires. Returning to the prior phase and the intended handling of a tour de
table need explicit implementation. Until then, a chair uses only supported
events and the server validates every request against the current phase.

### 5. Vote

WebMUN currently supports two distinct voting mechanisms:

- **Procedural voting:** accepting a submitted motion creates a vote. Closing
  it tallies the vote and applies the supported motion transition, or restores
  the previous phase.
- **Informal voting:** the chair may open a named, non-procedural vote. It
  uses `Voting Execution` temporarily and returns to its origin phase when
  closed; it does not itself apply a procedural transition.

An accepted end-debate motion enters `Voting Preparation`. The chair then uses
`StartResolutionVoteEvent` to start the first `DRAFT` item in
`draft_resolutions`, in list order. The session enters `Voting Procedures`.

Before a resolution's substantive vote, each pending unfriendly amendment on
that resolution is voted procedurally in submission order. A passed amendment
becomes adopted; a failed amendment becomes rejected. Friendly amendments are
accepted directly when the chair accepts their introduction.

The substantive vote has two forms:

- **Standard vote:** each eligible delegate may submit `Favour`, `Against`, or
  `Abstain`; the chair may record a vote on a delegation's behalf and closes
  the vote with `CloseSubstantiveVotingEvent`.
- **Roll-call vote:** a passed `Vote By Roll Call` motion marks one draft for
  roll call. Every representation marked `Present` or `Present and Voting` in
  the completed roll call must vote. The initial round also accepts
  `Yes With Rights` and `No With Rights`. The chair advances through the yes
  and no rights queues using `AdvanceSubstantiveVoteRoundEvent`; the existing
  floor controls serve each queued representation for 30 seconds.

`Present and Voting` representations cannot abstain. A terminal substantive
vote returns to `Voting Preparation`, where the chair may start the next draft
when one is available.

### Resolution preparation motions

Delegates submit resolution-related motion fields as strings. The chair must
accept the introduction before the draft enters live state; acceptance is the
formatting and procedural gate.

- Resolution introduction requires `resolution_id` and `resolution_title`.
- Amendment introduction requires `target_resolution_id`, `amendment_id`, and
  `is_friendly`.
- Split Proposal requires `target_resolution_id`, `split_resolution_id`, and
  `split_title`. When passed in Voting Preparation, it retains the parent and
  appends a child draft with the parent's submitter and roll-call setting.
- Vote By Roll Call requires `target_resolution_id` and, when passed in Voting
  Preparation, marks only that draft for a roll-call substantive vote.

`VOTE_AMENDMENT` is not an available motion. Pending unfriendly amendments are
handled automatically as part of their target resolution's vote.

### 6. Close the session

The chair can send `CloseSessionEvent` from the phases accepted by the engine,
which clears active debate and timer state and moves the session to `Finished`.

## Technical approach

### One authoritative state machine

`SessionLiveState` is the active committee state machine. A transition reads
the current state, verifies the actor and payload, and updates this state. This
makes a single server—not several browser tabs—the authority for speaker
order, attendance, votes, and phase transitions.

The state includes both the phase and the context required to continue it:

- `delegations`, keyed by `representation_id`;
- roll-call and voting eligibility;
- GSL, current speaker, and timer;
- caucus/debate context;
- submitted motions and questions; and
- the current voting context and the phase to return to.

Draft resolution and amendment terminal statuses are currently kept in the
live snapshot so connected clients can render the result. There is not yet a
separate durable audit/event stream. A future audit implementation should move
terminal outcomes and tallies out of the live draft list and notify clients
with explicit result events.

### Commands in, snapshots out

Clients connect to the session WebSocket, authenticate with a Supabase JWT,
and receive a complete initial snapshot. They send an event envelope such as
`{ "type": "JoinQueueEvent", "payload": {} }`. The WebSocket handler builds a
server-side actor from the JWT and committee assignment, dispatches the event
to the session engine, then broadcasts the next complete snapshot.

```text
authenticated client request
  -> WebSocket handler builds SessionActor
  -> engine validates role, representation IDs, and current phase
  -> in-memory SessionLiveState changes
  -> updated snapshot is broadcast to all connected clients
```

The frontend replaces its shared session state with each received snapshot. It
does not optimistically edit the shared state, because another accepted event
may have changed the phase or queue first. This is also why a UI permission
check is a convenience only; authorization is enforced by the backend.

### Persistence boundary today

Activating a session stores its initial snapshot in PostgreSQL, and a missing
in-memory room can be reconstructed from that stored snapshot. The current
per-event handler updates `ConnectionManager.room_states` and broadcasts it,
but does **not** persist the changed snapshot after every accepted event.
Consequently, a process restart can recover the last stored snapshot rather
than the latest live action. Persisting accepted state atomically before (or
with) broadcast is required before durable live-session recovery can be
claimed.

### Extending the flow safely

When adding a new committee rule, define its phase preconditions, actor role,
required `representation_id` references, state transition, and recovery or
persistence impact before adding a UI control. Add the event schema and engine
handler together, then document the flow change here and in the event
reference. Because live snapshots are persisted, changes to
`SessionLiveState` need a compatibility or migration path. Event persistence
should be part of that design, rather than being left to the frontend.

## Related references

- [Real-time overview](overview.md) explains the WebSocket protocol.
- [Events and payloads](events-and-payloads.md) is the event-level reference.
- [Session state](session-state.md) lists the snapshot fields.
- [Architecture](../architecture.md) explains the frontend, backend, and
  persistence boundaries.
