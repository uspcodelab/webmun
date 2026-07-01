import { screen } from "@testing-library/react"
import { beforeEach, describe, expect, it } from "vitest"

import DelegationMap from "@/components/session/delegation-map"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { createSessionState } from "@/test/session-state"
import { renderWithRouter } from "@/test/render"

describe("DelegationMap", () => {
  beforeEach(() => {
    useCommitteeStore.setState(createSessionState(), true)
  })

  it("renders quorum, state, and majority summaries from store state", () => {
    renderWithRouter(
      <DelegationMap semicircleCount={1} buttonsPerSemicircle={[3]} />,
    )

    expect(screen.getByText("2/3 delegações")).toBeInTheDocument()
    expect(screen.getByText("Open GSL")).toBeInTheDocument()
    expect(screen.getByText("Maioria simples: 2 votos")).toBeInTheDocument()
    expect(screen.getByText("Maioria qualificada: 2 votos")).toBeInTheDocument()
  })
})
