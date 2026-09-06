import * as React from "react"

import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useConference } from "@/context/ConferenceContext"
import { apiJson } from "@/lib/api"

type Allocation = { email: string; committee_id: number | null; committee_name: string | null; representation_id: number | null; representation_name: string | null }
type Representation = { id: number; name: string; code: string | null }
type Choice = { committeeId: string; representationId: string }

export default function ParticipantListAllocation() {
  const { activeConferenceId, committees } = useConference()
  const [allocations, setAllocations] = React.useState<Allocation[]>([])
  const [choices, setChoices] = React.useState<Record<string, Choice>>({})
  const [representations, setRepresentations] = React.useState<Record<number, Representation[]>>({})
  const [error, setError] = React.useState<string | null>(null)
  const [saving, setSaving] = React.useState(false)

  const load = React.useCallback(async () => {
    if (!activeConferenceId) return setAllocations([])
    try {
      const values = await apiJson<Allocation[]>(`/conferences/${activeConferenceId}/participants/allocations`)
      setAllocations(values)
      setChoices(Object.fromEntries(values.map((item) => [item.email, { committeeId: item.committee_id ? String(item.committee_id) : "", representationId: item.representation_id ? String(item.representation_id) : "" }])))
      const committeeIds = [...new Set(values.flatMap((item) => item.committee_id ? [item.committee_id] : []))]
      const seats = await Promise.all(committeeIds.map(async (committeeId) => [committeeId, await apiJson<Representation[]>(`/committees/${committeeId}/representations`)] as const))
      setRepresentations(Object.fromEntries(seats))
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

  const pendingAllocations = allocations.filter((allocation) => {
    const choice = choices[allocation.email]
    return choice?.committeeId && choice.representationId && (
      choice.committeeId !== String(allocation.committee_id ?? "") ||
      choice.representationId !== String(allocation.representation_id ?? "")
    )
  })

  async function saveAll() {
    if (!activeConferenceId || pendingAllocations.length === 0) return
    setSaving(true); setError(null)
    try {
      await Promise.all(pendingAllocations.map((allocation) => {
        const choice = choices[allocation.email]
        if (!choice) return Promise.resolve()
        return apiJson(`/conferences/${activeConferenceId}/participants/allocations`, { method: "PUT", body: JSON.stringify({ email: allocation.email, committee_id: Number(choice.committeeId), representation_id: Number(choice.representationId) }) })
      }))
      await load()
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível salvar as alocações") }
    finally { setSaving(false) }
  }

  return <section className="space-y-5">
    <div><h1 className="text-2xl font-bold">Listagem e alocação de participantes</h1><p className="text-muted-foreground">Participantes adicionados à conferência aparecem aqui para alocação em comitês.</p></div>
    {!activeConferenceId ? <p className="text-muted-foreground">Selecione uma conferência.</p> : <>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <div className="flex justify-end"><Button disabled={saving || pendingAllocations.length === 0} onClick={() => void saveAll()}>{saving ? "Salvando..." : `Salvar alocações${pendingAllocations.length ? ` (${pendingAllocations.length})` : ""}`}</Button></div>
      <div className="overflow-x-auto rounded-xl border"><table className="w-full text-sm"><thead><tr className="border-b text-left"><th className="p-3">E-mail</th><th className="p-3">Comitê</th><th className="p-3">Representação</th></tr></thead><tbody>{allocations.map((allocation) => {
        const choice = choices[allocation.email] ?? { committeeId: "", representationId: "" }
        const seats = representations[Number(choice.committeeId)] ?? []
        return <tr key={`${allocation.email}-${allocation.committee_id ?? "none"}`} className="border-b last:border-0"><td className="p-3">{allocation.email}</td><td className="p-3"><Select value={choice.committeeId} onValueChange={(value) => void chooseCommittee(allocation.email, value)}><SelectTrigger className="w-52"><SelectValue placeholder={allocation.committee_name ?? "Selecionar comitê"} /></SelectTrigger><SelectContent>{committees.map((committee) => <SelectItem key={committee.id} value={String(committee.id)}>{committee.name}</SelectItem>)}</SelectContent></Select></td><td className="p-3"><Select value={choice.representationId} disabled={!choice.committeeId} onValueChange={(value) => setChoices((current) => ({ ...current, [allocation.email]: { ...choice, representationId: value } }))}><SelectTrigger className="w-52"><SelectValue placeholder={allocation.representation_name ?? "Selecionar representação"} /></SelectTrigger><SelectContent>{seats.map((seat) => <SelectItem key={seat.id} value={String(seat.id)}>{seat.name}</SelectItem>)}</SelectContent></Select></td></tr>
      })}{allocations.length === 0 ? <tr><td colSpan={3} className="p-6 text-center text-muted-foreground">Nenhum participante adicionado.</td></tr> : null}</tbody></table></div>
    </>}
  </section>
}
