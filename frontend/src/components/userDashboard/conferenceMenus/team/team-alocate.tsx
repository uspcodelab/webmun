import * as React from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useConference } from "@/context/ConferenceContext"
import { apiJson } from "@/lib/api"

type Assignment = { conference_id: number; email: string; role: string; committee_id: number | null }

const roles = ["secretary_general", "director", "moderator", "rapporteur", "crisis_staff", "press", "logistics", "staff", "participant"]

export default function TeamAllocate() {
  const { activeConferenceId, committees } = useConference()
  const [assignments, setAssignments] = React.useState<Assignment[]>([])
  const [email, setEmail] = React.useState("")
  const [role, setRole] = React.useState("participant")
  const [committeeId, setCommitteeId] = React.useState<string>("none")
  const [error, setError] = React.useState<string | null>(null)
  const [saving, setSaving] = React.useState(false)

  const load = React.useCallback(async () => {
    if (!activeConferenceId) return setAssignments([])
    try {
      setAssignments(await apiJson<Assignment[]>(`/conferences/${activeConferenceId}/assignments`))
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Não foi possível carregar a equipe")
    }
  }, [activeConferenceId])

  React.useEffect(() => { void load() }, [load])

  async function submit(event: React.FormEvent) {
    event.preventDefault()
    if (!activeConferenceId) return
    setSaving(true)
    setError(null)
    try {
      await apiJson(`/conferences/${activeConferenceId}/assignments`, {
        method: "POST",
        body: JSON.stringify({ email, role, committee_id: committeeId === "none" ? null : Number(committeeId) }),
      })
      setEmail("")
      setCommitteeId("none")
      await load()
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Não foi possível adicionar a pessoa")
    } finally { setSaving(false) }
  }

  return <section className="space-y-5">
    <div><h1 className="text-2xl font-bold">Adicionar e alocar equipe</h1><p className="text-muted-foreground">Adicione por e-mail e atribua um papel real na conferência.</p></div>
    {!activeConferenceId ? <p className="text-muted-foreground">Selecione uma conferência.</p> : <>
      <form onSubmit={submit} className="flex flex-col gap-3 rounded-xl border p-4 md:flex-row md:items-end">
        <label className="grid flex-1 gap-1 text-sm">E-mail<Input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label>
        <label className="grid gap-1 text-sm">Papel<Select value={role} onValueChange={setRole}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{roles.map((item) => <SelectItem key={item} value={item}>{item}</SelectItem>)}</SelectContent></Select></label>
        <label className="grid gap-1 text-sm">Comitê (opcional)<Select value={committeeId} onValueChange={setCommitteeId}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="none">Toda a conferência</SelectItem>{committees.map((committee) => <SelectItem key={committee.id} value={String(committee.id)}>{committee.name}</SelectItem>)}</SelectContent></Select></label>
        <Button disabled={saving}>{saving ? "Adicionando..." : "Adicionar"}</Button>
      </form>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <div className="overflow-hidden rounded-xl border"><table className="w-full text-sm"><thead><tr className="border-b text-left"><th className="p-3">E-mail</th><th className="p-3">Papel</th><th className="p-3">Comitê</th></tr></thead><tbody>{assignments.map((assignment) => <tr className="border-b last:border-0" key={`${assignment.email}-${assignment.role}-${assignment.committee_id}`}><td className="p-3">{assignment.email}</td><td className="p-3">{assignment.role}</td><td className="p-3">{committees.find((committee) => committee.id === assignment.committee_id)?.name ?? "Toda a conferência"}</td></tr>)}{assignments.length === 0 ? <tr><td className="p-6 text-center text-muted-foreground" colSpan={3}>Nenhuma pessoa adicionada.</td></tr> : null}</tbody></table></div>
    </>}
  </section>
}
