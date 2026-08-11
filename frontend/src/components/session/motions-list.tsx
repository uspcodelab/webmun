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
import { sendMessage,useSession } from "@/context/SessionContext"
import { SessionRoles, ChairEvents, type ResolveMotionEvent} from "@/schemas/types.gen"
import { useCommitteeStore } from "@/store/useCommitteeStore"


export default function MotionsList() {
    const {role} = useSession()
    const isChair = role===SessionRoles.CHAIR

    const motions = useCommitteeStore((state)=>state.submitted_motions)!
    const delegations = useCommitteeStore((state)=>state.delegations)

    const sortedMotions = [...motions].sort((a, b) => {
        if(b.priority !== a.priority) return b.priority! - a.priority!

        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
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
                            <h2 className="font-bold text-black text-xs">{new Date(motion.timestamp).toLocaleTimeString('pt-BR', {
  hour: '2-digit',
  minute: '2-digit'
})}</h2>
                        </div>
                    </ItemMedia>
                    <ItemContent>
                        <ItemTitle>{motion.type}</ItemTitle>
                        <ItemDescription className="flex items-center gap-2">
                            <Flags code={motion.delegate_id ? motion.delegate_id.toString() : "0"} className="h-4" />
                            <span>{delegations[motion.delegate_id!].name}</span>
                        </ItemDescription>
                    </ItemContent>
                    <ItemFooter className="flex-col items-stretch gap-2 pt-2">
                        {isChair && (
                            <div className="flex items-center gap-2">
                                <Button size="sm" className="flex-1 bg-green-800 text-white hover:bg-green-700"
                                onClick={()=>sendMessage({type:ChairEvents.RESOLVE_MOTION_EVENT, payload:{motion_id:motion.id!, action:true }} satisfies ResolveMotionEvent)}>Acatar</Button>
                                <Button size="sm" className="flex-1 bg-red-800 text-white hover:bg-red-700"
                                onClick={()=>sendMessage({type:ChairEvents.RESOLVE_MOTION_EVENT, payload:{motion_id:motion.id!, action:false }} satisfies ResolveMotionEvent)}>Rejeitar</Button>
                            </div>
                        )}
                        <Separator />
                    </ItemFooter>
                </Item>
            ))}
        </ScrollArea>

    </div>)
}