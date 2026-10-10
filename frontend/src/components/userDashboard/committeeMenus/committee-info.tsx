import { useParams } from "react-router-dom"

import { useConference } from "@/context/ConferenceContext"

export default function CommitteeInfo() {
  const { committeeId } = useParams()
  const { committees } = useConference()
  const committee = committees.find((item) => item.id === Number(committeeId))

  if (!committee) return <p className="text-muted-foreground">Comitê não encontrado.</p>

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">{committee.name}</h1>
      <p className="text-muted-foreground">
        Such Info! much knowledge.
      </p>
    </div>
  )
}
