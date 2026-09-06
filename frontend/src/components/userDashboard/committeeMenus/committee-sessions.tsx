import * as React from "react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useConference } from "@/context/ConferenceContext"
import { apiFetch, apiJson } from "@/lib/api"
import { useNavigate } from "react-router-dom"

type CommitteeSession = { id: number; committee_id: number; name: string | null; status: string; started_at: string | null; ended_at: string | null }

export default function CommitteeSessions() {
  const { activeCommittee, activeCommitteeAccess } = useConference()
  const navigate = useNavigate()
  const [sessions, setSessions] = React.useState<CommitteeSession[]>([])
  const [name, setName] = React.useState("")
  const [error, setError] = React.useState<string | null>(null)
  const [creating, setCreating] = React.useState(false)
  const [activating, setActivating] = React.useState<number | null>(null)
  const canManage = activeCommitteeAccess?.role === "chair"

  const load = React.useCallback(async () => {
    if (!activeCommittee) return setSessions([])
    try { setSessions(await apiJson<CommitteeSession[]>(`/sessions/committee/${activeCommittee.id}`)) }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível carregar sessões") }
  }, [activeCommittee])

  React.useEffect(() => { void load() }, [load])

  async function create(event: React.FormEvent) {
    event.preventDefault()
    if (!activeCommittee) return
    setCreating(true); setError(null)
    try {
      await apiJson("/sessions/", { method: "POST", body: JSON.stringify({ committee_id: activeCommittee.id, name: name || null }) })
      setName(""); await load()
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível criar a sessão") }
    finally { setCreating(false) }
  }

  async function activate(id: number) {
    setActivating(id); setError(null)
    try {
      const response = await apiFetch(`/sessions/${id}/activate`, { method: "POST" })
      if (!response.ok) throw new Error((await response.text()) || "Não foi possível ativar a sessão")
      await load()
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Não foi possível ativar a sessão") }
    finally { setActivating(null) }
  }

  return <section className="space-y-5">
    <div><h1 className="text-2xl font-bold">Sessões {activeCommittee ? `— ${activeCommittee.name}` : ""}</h1><p className="text-muted-foreground">Crie e ative sessões reais deste comitê.</p></div>
    {!activeCommittee ? <p className="text-muted-foreground">Selecione um comitê.</p> : <>
      {canManage ? <form onSubmit={create} className="flex gap-2"><Input value={name} onChange={(event) => setName(event.target.value)} placeholder="Nome da sessão (opcional)" /><Button disabled={creating}>{creating ? "Criando..." : "Criar sessão"}</Button></form> : null}
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <div className="space-y-2">{sessions.map((session) => <article key={session.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border p-4"><div><p className="font-medium">{session.name || `Sessão ${session.id}`}</p><Badge variant={session.status === "active" ? "default" : "secondary"}>{session.status}</Badge></div><div className="flex gap-2">{canManage && session.status === "planned" ? <Button variant="outline" disabled={activating === session.id} onClick={() => void activate(session.id)}>{activating === session.id ? "Ativando..." : "Ativar"}</Button> : null}<Button disabled={session.status !== "active"} onClick={() => navigate(`/sessions/${session.id}`)}>Entrar</Button></div></article>)}{sessions.length === 0 ? <p className="rounded-xl border p-6 text-center text-muted-foreground">Nenhuma sessão criada.</p> : null}</div>
    </>}
  </section>
}
