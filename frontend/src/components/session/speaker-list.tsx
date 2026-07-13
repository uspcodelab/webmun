import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Item,
    ItemContent,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import { Badge } from "@/components/ui/badge"
import Flags from "@/components/ui/flags"
import { useCommitteeStore } from "@/store/useCommitteeStore"

const isChair = true // Replace with actual logic to determine if the user is the chair
const isAlredyInQueue = true // Replace with actual logic to determine if the user is already in the queue
//TODO determine if queue is open, if not obscure the button and show a message that the queue is closed

export default function SpeakerList() {
    const gslQueue = useCommitteeStore((state) => state.gsl_queue ?? [])
    const currentSpeaker = useCommitteeStore((state) => state.current_speaker)
    const waitingCount = gslQueue.length


    return (<div className="flex min-h-0 flex-1 flex-col">
        <div className="m-4 flex items-center">
            <h2 className="text-xl font-bold">Lista de Oradores</h2>
            <Badge className="ml-auto bg-tertiary-200 text-secondary">{String(waitingCount).padStart(2, "0")} em espera</Badge>
        </div>
        <ScrollArea className="mr-4 mb-2 ml-4 mt-0 min-h-0 flex-1 rounded-md border ">
            {gslQueue.map((delegate, index) => {
                const isSpeaking = !!currentSpeaker && currentSpeaker.id === delegate.id
                const position = index + 1

                return (
                    <div key={delegate.id}>
                        <Item size="sm" className="mb-0">
                            <ItemMedia
                                variant="icon"
                                className={`${isSpeaking ? "bg-secondary" : "bg-neutral-100"} h-10 w-10 rounded-full`}
                            >
                                <div className="h-10 mb-0 items-center justify-center flex">
                                    <h2 className={`font-bold text-lg ${isSpeaking ? "text-white" : "text-secondary"}`}>
                                        {String(position).padStart(2, "0")}
                                    </h2>
                                </div>
                            </ItemMedia>
                            <ItemContent>
                                <ItemTitle>
                                    {delegate.name}
                                    <Flags code={delegate.code} className="h-5" />
                                </ItemTitle>
                            </ItemContent>
                        </Item>
                        {index < gslQueue.length - 1 && (
                            <Separator className="mx-4" />
                        )}
                    </div>
                )
            })}
        </ScrollArea>
        {!isChair && (
            <Button variant="outline" className="mr-4 mb-2 ml-4" disabled={isAlredyInQueue}> 
                Se colocar na lista de oradores
            </Button>
        )}
        {isChair && (
            <Button variant="outline" className="mr-4 mb-2 ml-4" disabled={waitingCount === 0} > 
                Dar a palavra ao próximo orador
            </Button>
        )}
        <Separator></Separator>
        
    </div>)
}