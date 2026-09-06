import { useConference } from "@/context/ConferenceContext"
import { Navigate } from "react-router-dom"

export default function ConferenceOverview() {
  const { activeConference } = useConference()

  if (!activeConference) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">{activeConference.name}</h1>
      <p className="text-muted-foreground">Visão geral da conferência.</p>
    </div>
  )
}
