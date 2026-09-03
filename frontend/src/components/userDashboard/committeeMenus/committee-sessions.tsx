
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
    Item,
    ItemActions,
    ItemContent,
    ItemDescription,
    ItemGroup,
    ItemHeader,
    ItemTitle,
} from "@/components/ui/item"
import { useConference } from "@/context/ConferenceContext"
import { apiFetch } from "@/lib/api"
import * as React from "react"

type CommitteeSession = {
    id: string
    sessionNumber: number
    startTime: string
    endTime: string
    status?: "planned" | "active"
    joinHref?: string
}

type CommitteeSessionsProps = {
    sessions?: CommitteeSession[]
    onJoin?: (session: CommitteeSession) => void
}

const defaultSessions: CommitteeSession[] = [
    {
        id: "1",
        sessionNumber: 1,
        startTime: "09:00",
        endTime: "10:30",
        status: "planned",
        joinHref: "/sessions/1",
    },
    {
        id: "2",
        sessionNumber: 2,
        startTime: "11:00",
        endTime: "12:30",
        status: "planned",
        joinHref: "/sessions/2",
    },
    {
        id: "3",
        sessionNumber: 3,
        startTime: "14:00",
        endTime: "15:30",
        status: "planned",
        joinHref: "/sessions/3",
    },
]

export default function CommitteeSessions({
    sessions = defaultSessions,
    onJoin,
}: CommitteeSessionsProps) {
    const { activeCommittee, activeCommitteeAccess } = useConference()
    const [activatedSessionIds, setActivatedSessionIds] = React.useState<Set<string>>(
        () =>
            new Set(
                sessions
                    .filter((session) => session.status === "active")
                    .map((session) => session.id)
            )
    )
    const [activatingSessionId, setActivatingSessionId] = React.useState<
        string | null
    >(null)
    const [activationError, setActivationError] = React.useState<string | null>(null)
    const canActivateSessions = activeCommitteeAccess?.role === "chair"

    async function activateSession(session: CommitteeSession) {
        setActivatingSessionId(session.id)
        setActivationError(null)

        try {
            const response = await apiFetch(`/sessions/${session.id}/activate`, {
                method: "POST",
            })

            if (!response.ok) {
                const errorText = await response.text()
                throw new Error(errorText || "Failed to activate session")
            }

            setActivatedSessionIds((currentIds) => new Set(currentIds).add(session.id))
        } catch (error) {
            setActivationError(
                error instanceof Error ? error.message : "Failed to activate session"
            )
        } finally {
            setActivatingSessionId(null)
        }
    }

    return (
        <section className="w-full space-y-4">
            <header className="space-y-1">
                <h2 className="text-2xl font-semibold tracking-tight">
                    {activeCommittee?.name ?? "Committee"} Sessions
                </h2>
                <p className="text-sm text-muted-foreground">
                    View session time windows and join active sessions.
                </p>
            </header>

            {activationError ? (
                <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
                    {activationError}
                </div>
            ) : null}

            <ItemGroup className="gap-2">
                {sessions.map((session) => {
                    const sessionIsActive = activatedSessionIds.has(session.id)

                    return (
                        <Item
                            key={session.id}
                            variant="outline"
                            className="justify-between gap-3 p-3"
                        >
                            <ItemHeader className="flex w-full flex-col items-start gap-3 md:flex-row md:items-center md:justify-between">
                                <ItemContent className="min-w-0 gap-0.5">
                                    <ItemTitle>
                                        <div className="flex flex-wrap items-center gap-2">
                                            <Badge variant="secondary">
                                                Session {session.sessionNumber}
                                            </Badge>
                                            {sessionIsActive ? <Badge>Active</Badge> : null}
                                        </div>
                                    </ItemTitle>
                                    <ItemDescription>
                                        Start: {session.startTime} | End: {session.endTime}
                                    </ItemDescription>
                                </ItemContent>

                                <ItemActions className="w-full justify-start md:w-auto md:justify-end">
                                    {canActivateSessions ? (
                                        <Button
                                            variant="outline"
                                            onClick={() => void activateSession(session)}
                                            disabled={
                                                sessionIsActive ||
                                                activatingSessionId === session.id
                                            }
                                        >
                                            {activatingSessionId === session.id
                                                ? "Activating..."
                                                : "Activate"}
                                        </Button>
                                    ) : null}
                                    {session.joinHref ? (
                                        <Button asChild>
                                            <a href={session.joinHref}>Join</a>
                                        </Button>
                                    ) : (
                                        <Button onClick={() => onJoin?.(session)}>
                                            Join
                                        </Button>
                                    )}
                                </ItemActions>
                            </ItemHeader>
                        </Item>
                    )
                })}
            </ItemGroup>
        </section>
    )
}
