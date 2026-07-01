import { render } from "@testing-library/react"
import type { ReactElement } from "react"
import { MemoryRouter } from "react-router-dom"

export function renderWithRouter(
  ui: ReactElement,
  initialEntries: string[] = ["/"],
) {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      {ui}
    </MemoryRouter>,
  )
}
