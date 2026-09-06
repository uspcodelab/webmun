import * as React from "react"

import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useConference } from "@/context/ConferenceContext"
import { apiJson } from "@/lib/api"

type Allocation = { email: string; committee_id: number | null; committee_name: string | null; representation_id: number | null; representation_name: string | null }
type Representation = { id: number; name: string; code: string | null }

export default function ParticipantListAllocation() {
  const { activeConferenceId, committees } = useConference()
  const [allocations, setAllocations] = React.useState<Allocation[]>([])
  const [choices, setChoices] = React.useState<Record<string, { committeeId: string; representationId: string }>>({})
  const [representations, setRepresentations] = React.useState<Record<number, Representation[]>>({})
  const [error, setError] = React.useState<string | null>(null)
  const [saving, setSaving] = React.useState<string | null>(null)

  const load = React.useCallback(async () => {
    if (!activeConferenceId) return setAllocations([])
    try {
      const values = await apiJson<Allocation[]>(`/conferences/${activeConferenceId}/participants/allocations`)
      setAllocations(values)
      setChoices(Object.fromEntries(values.map((item) => [item.email, { committeeId: item.committee_id ? String(item.committee_id) : "", representationId: item.representation_id ? String(item.representation_id) : "" }])))
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível carregar participantes") }
  }, [activeConferenceId])

  React.useEffect(() => { void load() }, [load])

  async function chooseCommittee(email: string, committeeId: string) {
    setChoices((current) => ({ ...current, [email]: { committeeId, representationId: "" } }))
    if (!committeeId || representations[Number(committeeId)]) return
    try {
      const seats = await apiJson<Representation[]>(`/committees/${committeeId}/representations`)
      setRepresentations((current) => ({ ...current, [Number(committeeId)]: seats }))
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível carregar representações") }
  }

  async function save(email: string) {
    const choice = choices[email]
    if (!activeConferenceId || !choice?.committeeId || !choice.representationId) return
    setSaving(email); setError(null)
    try {
      await apiJson(`/conferences/${activeConferenceId}/participants/allocations`, { method: "PUT", body: JSON.stringify({ email, committee_id: Number(choice.committeeId), representation_id: Number(choice.representationId) }) })
      await load()
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível salvar a alocação") }
    finally { setSaving(null) }
  }

  return <section className="space-y-5">
    <div><h1 className="text-2xl font-bold">Listagem e alocação de participantes</h1><p className="text-muted-foreground">Participantes adicionados à conferência aparecem aqui para alocação em comitês.</p></div>
    {!activeConferenceId ? <p className="text-muted-foreground">Selecione uma conferência.</p> : <>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <div className="overflow-x-auto rounded-xl border"><table className="w-full text-sm"><thead><tr className="border-b text-left"><th className="p-3">E-mail</th><th className="p-3">Comitê</th><th className="p-3">Representação</th><th className="p-3" /></tr></thead><tbody>{allocations.map((allocation) => {
        const choice = choices[allocation.email] ?? { committeeId: "", representationId: "" }
        const seats = representations[Number(choice.committeeId)] ?? []
        return <tr key={`${allocation.email}-${allocation.committee_id ?? "none"}`} className="border-b last:border-0"><td className="p-3">{allocation.email}</td><td className="p-3"><Select value={choice.committeeId} onValueChange={(value) => void chooseCommittee(allocation.email, value)}><SelectTrigger className="w-52"><SelectValue placeholder={allocation.committee_name ?? "Selecionar comitê"} /></SelectTrigger><SelectContent>{committees.map((committee) => <SelectItem key={committee.id} value={String(committee.id)}>{committee.name}</SelectItem>)}</SelectContent></Select></td><td className="p-3"><Select value={choice.representationId} disabled={!choice.committeeId} onValueChange={(value) => setChoices((current) => ({ ...current, [allocation.email]: { ...choice, representationId: value } }))}><SelectTrigger className="w-52"><SelectValue placeholder={allocation.representation_name ?? "Selecionar representação"} /></SelectTrigger><SelectContent>{seats.map((seat) => <SelectItem key={seat.id} value={String(seat.id)}>{seat.name}</SelectItem>)}</SelectContent></Select></td><td className="p-3"><Button size="sm" disabled={saving === allocation.email || !choice.committeeId || !choice.representationId} onClick={() => void save(allocation.email)}>{saving === allocation.email ? "Salvando..." : "Salvar"}</Button></td></tr>
      })}{allocations.length === 0 ? <tr><td colSpan={4} className="p-6 text-center text-muted-foreground">Nenhum participante adicionado.</td></tr> : null}</tbody></table></div>
    </>}
  </section>
}
