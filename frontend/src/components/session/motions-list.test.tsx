import { screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import MotionsList, { type Motion } from "@/components/session/motions-list"
import { renderWithRouter } from "@/test/render"

describe("MotionsList", () => {
  it("orders motions by priority descending and timestamp ascending", () => {
    const motions: Motion[] = [
      {
        id: "late-high",
        timestamp: "16:05",
        title: "Late high priority",
        proposer: "France",
        proposerCode: "fr",
        priority: 3,
      },
      {
        id: "low",
        timestamp: "15:00",
        title: "Low priority",
        proposer: "Brazil",
        proposerCode: "br",
        priority: 1,
      },
      {
        id: "early-high",
        timestamp: "15:58",
        title: "Early high priority",
        proposer: "Japan",
        proposerCode: "jp",
        priority: 3,
      },
    ]

    renderWithRouter(<MotionsList motions={motions} />)

    const earlyHigh = screen.getByText("Early high priority")
    const lateHigh = screen.getByText("Late high priority")
    const low = screen.getByText("Low priority")

    expect(
      earlyHigh.compareDocumentPosition(lateHigh) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy()
    expect(
      lateHigh.compareDocumentPosition(low) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy()
  })
})
