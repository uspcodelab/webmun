import { act, fireEvent, screen } from "@testing-library/react"
import { beforeEach, describe, expect, it, vi } from "vitest"

import { ChairEvents } from "@/schemas/types.gen"
import Timer from "@/components/session/timer"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { createSessionState } from "@/test/session-state"
import { renderWithRouter } from "@/test/render"

const sendMessage = vi.fn()

vi.mock("@/pages/Session", () => ({
  sendMessage: (data: unknown) => sendMessage(data),
}))

describe("Timer", () => {
  beforeEach(() => {
    sendMessage.mockClear()
    vi.useRealTimers()
    useCommitteeStore.setState(createSessionState(), true)
  })

  it("renders the paused timer and sends chair timer events", () => {
    useCommitteeStore.setState(
      createSessionState({ timer_remaining_seconds: 65 }),
      true,
    )

    renderWithRouter(<Timer />)

    expect(screen.getByText("01:05")).toBeInTheDocument()
    expect(screen.getByText("Mesa")).toBeInTheDocument()

    fireEvent.click(screen.getByRole("button", { name: /start timer/i }))
    expect(sendMessage).toHaveBeenCalledWith({
      type: ChairEvents.TOGGLE_TIMER_EVENT,
      payload: {},
    })

    fireEvent.click(screen.getByRole("button", { name: /5s/i }))
    expect(sendMessage).toHaveBeenCalledWith({
      type: ChairEvents.INCREASE_TIMER_EVENT,
      payload: { seconds: 5 },
    })
  })

  it("counts down from timer_expiration while running", () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date("2026-07-01T12:00:00Z"))
    useCommitteeStore.setState(
      createSessionState({
        timer_is_running: true,
        timer_expiration: "2026-07-01T12:01:30Z",
        timer_remaining_seconds: 90,
      }),
      true,
    )

    renderWithRouter(<Timer />)

    expect(screen.getByText("01:30")).toBeInTheDocument()

    act(() => {
      vi.advanceTimersByTime(31_000)
    })

    expect(screen.getByText("00:59")).toBeInTheDocument()
  })
})
