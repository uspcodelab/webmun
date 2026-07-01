import { screen } from "@testing-library/react"
import { beforeEach, describe, expect, it } from "vitest"

import TopBar from "@/components/session/top-bar"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { createSessionState } from "@/test/session-state"
import { renderWithRouter } from "@/test/render"

describe("TopBar", () => {
  beforeEach(() => {
    useCommitteeStore.setState(createSessionState(), true)
  })

  it("shows the no-topic fallback", () => {
    renderWithRouter(<TopBar />)

    expect(screen.getByText("Nenhum tópico em discussão")).toBeInTheDocument()
  })

  it("shows the active agenda topic", () => {
    useCommitteeStore.setState(
      createSessionState({
        agenda_topics: [["Humanitarian corridors", false]],
        active_topic_index: 0,
      }),
      true,
    )

    renderWithRouter(<TopBar />)

    expect(screen.getByText("Humanitarian corridors")).toBeInTheDocument()
  })
})
