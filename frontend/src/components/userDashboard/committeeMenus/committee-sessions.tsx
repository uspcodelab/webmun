
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

type CommitteeSession = {
    id: string
    sessionNumber: number
    startTime: string
    endTime: string
    joinHref?: string
}

type CommitteeSessionsProps = {
    sessions?: CommitteeSession[]
    onJoin?: (session: CommitteeSession) => void
}

const defaultSessions: CommitteeSession[] = [
    {
        id: "session-1",
        sessionNumber: 1,
        startTime: "09:00",
        endTime: "10:30",
        joinHref: "/session/1",
    },
    {
        id: "session-2",
        sessionNumber: 2,
        startTime: "11:00",
        endTime: "12:30",
        joinHref: "/session/2",
    },
    {
        id: "session-3",
        sessionNumber: 3,
        startTime: "14:00",
        endTime: "15:30",
        joinHref: "/session/3",
    },
]

export default function CommitteeSessions({
    sessions = defaultSessions,
    onJoin,
}: CommitteeSessionsProps) {
    return (
        <section className="w-full space-y-4">
            <header className="space-y-1">
                <h2 className="text-2xl font-semibold tracking-tight">Committee Sessions</h2>
                <p className="text-sm text-muted-foreground">
                    View session time windows and join active sessions.
                </p>
            </header>

            <ItemGroup className="gap-2">
                {sessions.map((session) => (
                    <Item
                        key={session.id}
                        variant="outline"
                        className="justify-between gap-3 p-3"
                    >
                        <ItemHeader className="flex w-full flex-col items-start gap-3 md:flex-row md:items-center md:justify-between">
                            <ItemContent className="min-w-0 gap-0.5">
                                <ItemTitle>
                                    <Badge variant="secondary">Session {session.sessionNumber}</Badge>
                                </ItemTitle>
                                <ItemDescription>
                                    Start: {session.startTime} | End: {session.endTime}
                                </ItemDescription>
                            </ItemContent>

                            <ItemActions className="w-full justify-start md:w-auto md:justify-end">
                                {session.joinHref ? (
                                    <Button asChild>
                                        <a href={session.joinHref}>Join</a>
                                    </Button>
                                ) : (
                                    <Button onClick={() => onJoin?.(session)}>Join</Button>
                                )}
                            </ItemActions>
                        </ItemHeader>
                    </Item>
                ))}
            </ItemGroup>
        </section>
    )
}