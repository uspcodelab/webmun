import { useState } from "react"
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
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { sendMessage } from "@/context/SessionContext"
import { type EndSpeechEvent, type JoinQueueEvent, type NextSpeakerEvent, ChairEvents, DelegateEvents } from "@/schemas/types.gen"
import { useSession } from "@/context/SessionContext"
import { SessionRoles } from "@/schemas/types.gen"

export default function SpeakerList() {

    const { role, representation_id } = useSession()
    const isChair = role === SessionRoles.CHAIR
    const gslQueue = useCommitteeStore((state) => state.gsl_queue ?? [])
    const currentSpeaker = useCommitteeStore((state) => state.current_speaker)
    const delegationsById = useCommitteeStore((state) => state.delegations)

    const [cedingTime, setCedingTime] = useState(false)

    const timerRemaining = useCommitteeStore((state) => state.timer_remaining_seconds);
    const timerIsRunning = useCommitteeStore((state) => state.timer_is_running);
    const alreadyInQueue = representation_id ? gslQueue.includes(representation_id) : false
    const queuedDelegations = gslQueue.flatMap((delegationId) => {
        const delegation = delegationsById[String(delegationId)]
        return delegation ? [delegation] : []
    })
    const waitingCount = queuedDelegations.length


    return (
        <div className="flex min-h-0 flex-1 flex-col">
            <div className="m-4 flex items-center">
                <h2 className="text-xl font-bold">Lista de Oradores</h2>
                <Badge className="ml-auto bg-tertiary-200 text-secondary">{String(waitingCount).padStart(2, "0")} em espera</Badge>
            </div>
            <ScrollArea className="mr-4 mb-2 ml-4 mt-0 min-h-0 flex-1 rounded-md border ">
                {queuedDelegations.map((delegate, index) => {
                    const isSpeaking = currentSpeaker === delegate.id
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
                            {index < queuedDelegations.length - 1 && (
                                <Separator className="mx-4" />
                            )}
                        </div>
                    )
                })}
            </ScrollArea>
            {!isChair && (
                <Button
                    variant="outline"
                    className="mr-4 mb-2 ml-4 w-auto min-w-0 overflow-hidden text-ellipsis whitespace-nowrap"
                    disabled={alreadyInQueue}
                    onClick={() => sendMessage({ type: DelegateEvents.JOIN_QUEUE_EVENT, payload: {} } satisfies JoinQueueEvent)}
                >
                    Se colocar na lista de oradores
                </Button>
            )}
            {isChair && (
                <div className="ml-4 mr-4 mb-2   flex w-auto min-w-0 flex-col gap-2 overflow-hidden">
                    <div className="flex flex-row w-full gap-2">
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button
                                    variant="outline"
                                    className="flex-1 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap"
                                    disabled={waitingCount === 0}
                                    onClick={() => sendMessage({ type: ChairEvents.NEXT_SPEAKER_EVENT, payload: {} } satisfies NextSpeakerEvent)}
                                >
                                    <span className="md:hidden">Proximo</span>
                                    <span className="hidden md:inline">Proximo Orador</span>
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Passar para o próximo orador da lista</p>
                            </TooltipContent>
                        </Tooltip>
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button
                                    className="flex-1 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap bg-primary hover:bg-primary/90 text-white"
                                    disabled={currentSpeaker === null || timerRemaining === null || timerRemaining === undefined || timerRemaining <= 0 || timerIsRunning}
                                    onClick={() => {
                                        const mapSelectionEvent = new CustomEvent("mapselection", {
                                            detail: { type: cedingTime ? null : "cedetime" },
                                        })
                                        window.dispatchEvent(mapSelectionEvent)
                                        setCedingTime((value) => !value)
                                    }}
                                >
                                    {cedingTime ? (
                                        <>
                                            <span className="md:hidden">Cancelar Cessao</span>
                                            <span className="hidden md:inline">Cancelar Cessao de Tempo</span>
                                        </>
                                    ) : (
                                        <>
                                            <span className="md:hidden">Cessao</span>
                                            <span className="hidden md:inline">Cessao de Tempo</span>
                                        </>
                                    )}
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Ceder tempo restante a outra delegacao</p>
                            </TooltipContent>
                        </Tooltip>
                    </div>
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <Button  variant="destructive" disabled={currentSpeaker === null} className="flex-1 min-w-0 min-h-8 overflow-hidden text-ellipsis whitespace-nowrap "
                            onClick={()=>sendMessage({ type:ChairEvents.END_SPEECH_EVENT, payload: {}} satisfies EndSpeechEvent)}>
                                <span>Encerrar Fala</span>
                            </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Finalizar a fala atual e ceder o tempo a mesa</p>
                        </TooltipContent>
                    </Tooltip>


                </div>
            )}
            <Separator></Separator>

        </div>)
}
