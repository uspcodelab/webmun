import type { SessionLiveState } from "@/schemas/types.gen"
import { RollCallChoice, States } from "@/schemas/types.gen"

export function createSessionState(
  overrides: Partial<SessionLiveState> = {},
): SessionLiveState {
  return {
    session_id: 0,
    start_time: "2026-07-01T12:00:00Z",
    delegations: [
      { id: 0, name: "Brazil", seat: "1-1", code: "br" },
      { id: 1, name: "France", seat: "1-2", code: "fr" },
      { id: 2, name: "Japan", seat: "1-3", code: "jp" },
    ],
    current_state: States.OPEN_GSL,
    timer_is_running: false,
    timer_expiration: null,
    timer_remaining_seconds: 0,
    current_speaker: null,
    gsl_queue: [],
    can_set_motion: false,
    gsl_default_time_seconds: 60,
    caucus_list: [],
    debate: null,
    submitted_motions: [],
    submitted_questions: [],
    agenda_topics: [],
    active_topic_index: null,
    voting: null,
    voting_choice: null,
    roll_call: {
      registry: {
        0: RollCallChoice.PRESENT,
        1: RollCallChoice.PRESENT_AND_VOTING,
        2: RollCallChoice.ABSENT,
      },
      current_delegation: null,
    },
    ...overrides,
  }
}
