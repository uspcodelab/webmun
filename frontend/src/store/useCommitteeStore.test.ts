import { beforeEach, describe, expect, it } from "vitest"

import { States } from "@/schemas/types.gen"
import { createSessionState } from "@/test/session-state"

import { UpdateStore, useCommitteeStore } from "./useCommitteeStore"

const initialState = useCommitteeStore.getInitialState()

describe("useCommitteeStore", () => {
  beforeEach(() => {
    useCommitteeStore.setState(initialState, true)
  })

  it("starts with an empty committee projection", () => {
    const state = useCommitteeStore.getState()

    expect(state.session_id).toBe(-1)
    expect(state.delegations).toEqual([])
    expect(state.timer_is_running).toBe(false)
    expect(state.roll_call).toEqual({})
  })

  it("replaces local state with the backend session snapshot", () => {
    const snapshot = createSessionState({
      session_id: 42,
      current_state: States.ROLL_CALL,
      timer_remaining_seconds: 90,
      gsl_queue: [1, 2],
    })

    UpdateStore(snapshot)

    expect(useCommitteeStore.getState()).toMatchObject({
      session_id: 42,
      current_state: States.ROLL_CALL,
      timer_remaining_seconds: 90,
      gsl_queue: [1, 2],
    })
  })
})
