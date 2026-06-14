import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"

import {
    Item,
    ItemContent,
    ItemDescription,
    ItemFooter,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import { Badge } from "@/components/ui/badge"
import Flags from "@/components/ui/flags"

export type Motion = {
    id: string
    timestamp: string
    title: string
    proposer: string
    proposerCode: string
    priority: number
}

type MotionsListProps = {
    motions: Motion[]
}

export default function MotionsList({ motions }: MotionsListProps) {
    const toMinutes = (time: string): number => {
        const [hours, minutes] = time.split(":").map(Number)
        if (Number.isNaN(hours) || Number.isNaN(minutes)) {
            return Number.MAX_SAFE_INTEGER
        }
        return hours * 60 + minutes
    }

    const sortedMotions = [...motions].sort((a, b) => {
        if (b.priority !== a.priority) {
            return b.priority - a.priority
        }

        return toMinutes(a.timestamp) - toMinutes(b.timestamp)
    })
    const queueCount = sortedMotions.length

    return (<div className="m-4 flex min-h-0 flex-1 flex-col">
        <div className="flex items-center">
            <h2 className="text-xl font-bold">Moçoes Apresentadas</h2>
            <Badge className="ml-auto bg-tertiary-200 text-secondary">{String(queueCount).padStart(2, "0")} na fila</Badge>
        </div>
        <ScrollArea className="mt-4 min-h-0 flex-1 rounded-md border">
            {sortedMotions.map((motion) => (
                <Item size="sm" key={motion.id}>
                    <ItemMedia variant="icon" className="h-10 w-10 bg-neutral-200 rounded-full">
                        <div className="h-10 items-center justify-center flex">
                            <h2 className="font-bold text-black text-xs">{motion.timestamp}</h2>
                        </div>
                    </ItemMedia>
                    <ItemContent>
                        <ItemTitle>{motion.title}</ItemTitle>
                        <ItemDescription className="flex items-center gap-2">
                            <Flags code={motion.proposerCode} className="h-4" />
                            <span>{motion.proposer}</span>
                        </ItemDescription>
                    </ItemContent>
                    <ItemFooter className="flex-col items-stretch gap-2 pt-2">
                        <div className="flex items-center gap-2">
                            <Button size="sm" className="flex-1 bg-green-800 text-white hover:bg-green-700">Acatar</Button>
                            <Button size="sm" className="flex-1 bg-red-800 text-white hover:bg-red-700">Rejeitar</Button>
                        </div>
                        <Separator />
                    </ItemFooter>
                </Item>
            ))}
        </ScrollArea>

    </div>)
}