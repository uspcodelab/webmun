import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Item,
    ItemContent,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import Flags from "@/components/ui/flags"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { useSession } from "@/context/SessionContext"
import { SessionRoles } from "@/schemas/types.gen"

//TODO determine if queue is open, if not obscure the button and show a message that the queue is closed

export default function ModeratedDebate() {

    const { role } = useSession()
    const remainingDiscouses = useCommitteeStore((state) => state.debate?.total_speeches ?? null)
    const isChair = role === SessionRoles.CHAIR
    const gslQueue = useCommitteeStore((state) => state.gsl_queue ?? [])
    const currentSpeaker = useCommitteeStore((state) => state.current_speaker)
    const delegationsById = useCommitteeStore((state) => state.delegations)
    const queuedDelegations = gslQueue.flatMap((delegationId) => {
        const delegation = delegationsById[String(delegationId)]
        return delegation ? [delegation] : []
    })
    const waitingCount = queuedDelegations.length

    //TODO: Actually implement speaker history
    return (
        <div className="flex min-h-0 flex-1 flex-col">
            <div className="mr-4 mb-2 ml-4 mt-4 ">
                <h2 className="text-xl font-bold">Debate Moderado</h2>
                <p className="ml-auto text-muted-foreground">Historico de Oradores:</p>
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
                >
                    Quero me proniunciar
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
                                >
                                    <span className="md:hidden">Proximo</span>
                                    <span className="hidden md:inline">Proximo Orador</span>
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Escolher o próximo orador</p>
                            </TooltipContent>
                        </Tooltip>
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button className="flex-1 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap bg-primary hover:bg-primary/90 text-white">
                                    <span className="md:hidden">Cessao</span>
                                    <span className="hidden md:inline">Cessao de Tempo</span>
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Ceder tempo restante a outra delegacao</p>
                            </TooltipContent>
                        </Tooltip>
                    </div>
                    <div className="flex flex-row w-full gap-2">
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button variant="destructive" disabled={currentSpeaker === null} className="flex-1 min-w-0 min-h-8 overflow-hidden text-ellipsis whitespace-nowrap ">
                                    <span>Encerrar Fala</span>
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Finalizar a fala atual e ceder o tempo a mesa</p>
                            </TooltipContent>
                        </Tooltip>
                        <div className="flex flex-1 items-center justify-center px-2">
                            {remainingDiscouses && (
                                <p className="text-sm font-bold">
                                    {remainingDiscouses} discursos restantes
                                </p>
                            )}
                        </div>
                    </div>

                </div>
            )}
            <Separator></Separator>

        </div>)
}
