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

const isChair = true // Replace with actual logic to determine if the user is the chair

const agendaTopics = [
    [3, "Medidas de cooperacao internacional"],
    [1, "Atualizacao da situacao humanitaria"],
    [2, "Corredores de evacuacao"],
    ["2.2", "Corredores humanitarios prioritarios"],
    ["2.1.2", "Pontos de passagem seguros"],
    ["3.2", "Acordos de cooperacao regional"],
] as const

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

const sortedAgendaTopics = [...agendaTopics].sort((left, right) => compareTopicNumbers(left[0], right[0]))



export default function Agenda() {
    return (
        <Dialog>
            <DialogTrigger>
                Ver agenda
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
                        {sortedAgendaTopics.map(([topicNumber, topicName]) => (
                            <Item key={topicNumber}>
                                <ItemContent className={getTopicDepth(topicNumber) > 0 ? "pl-6" : undefined}>
                                    <ItemTitle>{topicNumber}. {topicName}</ItemTitle>
                                </ItemContent>
                                {isChair && (
                                    <ItemActions>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="outline" size="sm">
                                                    <MessagesSquare className="h-4 w-4" />
                                                </Button>
                                            </TooltipTrigger>
                                            <TooltipContent>
                                                <p>Topico em Discussão</p>
                                            </TooltipContent>
                                        </Tooltip>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="outline" size="sm">
                                                    <CircleCheckBig className="h-4 w-4" />
                                                </Button>
                                            </TooltipTrigger>
                                            <TooltipContent>
                                                <p>Topico ja Discutido</p>
                                            </TooltipContent>
                                        </Tooltip>
                                        <Tooltip>
                                            <TooltipTrigger asChild>
                                                <Button variant="destructive" size="sm">
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
                                <Input placeholder="Nº" className="w-12" />
                                <Input placeholder="Tópico" />
                            </div>

                            <Button className=" bg-green-800 text-white hover:bg-green-700">Adicionar</Button>
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog >
    )
}