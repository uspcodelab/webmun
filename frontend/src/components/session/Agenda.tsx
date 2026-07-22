import { sendMessage } from "@/pages/Session"
import type {SetAgendaItemEvent, MarkAgendaItemEvent, DeleteAgendaItemEvent} from "@/schemas/types.gen"
import {ChairEvents } from "@/schemas/types.gen"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Trash2, CircleCheckBig, MessagesSquare } from "lucide-react"
import {
    Dialog,
    DialogContent,
    DialogTrigger,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import {
    Item,
    ItemActions,
    ItemContent,
    ItemTitle,
} from "@/components/ui/item"
import { Input } from "@/components/ui/input"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip"

import { useRef } from "react"

export default function Agenda() {

    const isChair = true // Replace with actual logic to determine if the user is the chair

    const agendaTopics = useCommitteeStore((state) => state.agenda_topics)

    const numinput = useRef<HTMLInputElement>(null)
    const topicinput = useRef<HTMLInputElement>(null)

    const compareTopicNumbers = (left: number | string, right: number | string) => {
        const leftParts = String(left).split(".").map(Number)
        const rightParts = String(right).split(".").map(Number)
        const maxLength = Math.max(leftParts.length, rightParts.length)

        for (let index = 0; index < maxLength; index += 1) {
            const leftPart = leftParts[index] ?? 0
            const rightPart = rightParts[index] ?? 0

            if (leftPart !== rightPart) {
                return leftPart - rightPart
            }
        }

        return leftParts.length - rightParts.length
    }

    const getTopicDepth = (topicNumber: number | string) => String(topicNumber).split(".").length - 1


    const sortedAgendaTopics = Object.values(agendaTopics??{}).sort((left, right) => compareTopicNumbers(left.index, right.index))

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline">Ver Agenda</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Agenda do comite</DialogTitle>
                    <DialogDescription>
                        Veja a agenda do comite e os topicos que serao discutidos durante a sessao.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-2">
                    <ScrollArea className="h-75 w-full rounded-md border">
                        {sortedAgendaTopics.map(({index, topic}) => (
                            <Item key={index}>
                                <ItemContent className={getTopicDepth(index) > 0 ? "pl-6" : undefined}>
                                    <ItemTitle>{index}. {topic}</ItemTitle>
                                </ItemContent>
                                {isChair && (
                                    <ItemActions>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="outline" size="sm" onClick={() => sendMessage(
                                                    {type:ChairEvents.MARK_AGENDA_ITEM_EVENT, payload:{index: index,indiscussion:true}} as MarkAgendaItemEvent
                                                )}>
                                                    <MessagesSquare className="h-4 w-4" />
                                                </Button>
                                            </TooltipTrigger>
                                            <TooltipContent>
                                                <p>Topico em Discussão</p>
                                            </TooltipContent>
                                        </Tooltip>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="outline" size="sm" onClick={() => sendMessage(
                                                    {type:ChairEvents.MARK_AGENDA_ITEM_EVENT, payload:{index:index,discussed:true}} as MarkAgendaItemEvent
                                                )}>
                                                    <CircleCheckBig className="h-4 w-4" />
                                                </Button>
                                            </TooltipTrigger>
                                            <TooltipContent>
                                                <p>Topico ja Discutido</p>
                                            </TooltipContent>
                                        </Tooltip>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="destructive" size="sm" onClick={() => sendMessage(
                                                    {type:ChairEvents.DELETE_AGENDA_ITEM_EVENT, payload:{index: index}} as DeleteAgendaItemEvent
                                                )}>
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </TooltipTrigger>
                                            <TooltipContent>
                                                <p>Deletar Topico</p>
                                            </TooltipContent>
                                        </Tooltip>




                                    </ItemActions>
                                )}
                            </Item>
                        ))}
                    </ScrollArea>
                </div>
                {isChair && (
                    <div>
                        <Separator></Separator>

                        <div className="flex flex-col items-start gap-2">
                            <p>Adicionar tópico à agenda </p>
                            <p className="text-sm text-muted-foreground">
                                Nº deve ser no formato X.Y
                            </p>
                            <div className="flex w-full items-center gap-1">
                                <Input ref={numinput} placeholder="Nº" className="w-12" />
                                <Input ref={topicinput} placeholder="Tópico" />
                            </div>

                            <Button className=" bg-green-800 text-white hover:bg-green-700" onClick={
                                () => {
                                if(numinput.current && topicinput.current) {
                                    sendMessage({type:ChairEvents.SET_AGENDA_ITEM_EVENT, 
                                        payload:{index:numinput.current.value, topic: topicinput.current.value}} as SetAgendaItemEvent)
                                    numinput.current.value = ""
                                    topicinput.current.value = ""
                                }
                                }}>
                                Adicionar
                            </Button>
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog >
    )
}