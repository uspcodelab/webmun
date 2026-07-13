import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
import Timer from "./timer"
import { useState } from "react"
import { Trash2, CircleCheckBig } from "lucide-react"
import {
    Dialog,
    DialogContent,
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

const isChair = false // Replace with actual logic to determine if the user is the chair

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

export default function TopBar() {
    const [isAgendaOpen, setIsAgendaOpen] = useState(false)
    const activeTopicIndex = useCommitteeStore((state) => state.active_topic_index)
    const currentTopicLabel =
        activeTopicIndex !== null && activeTopicIndex !== undefined
            ? (sortedAgendaTopics[activeTopicIndex]?.[1] ?? "Nenhum tópico em discussão")
            : "Nenhum tópico em discussão"


    return (<>
        <div className="flex h-[10vh] w-full items-center shadow-lg px-4 py-2 relative z-10 ">
            <div className="flex h-full w-full flex-nowrap items-center gap-4 overflow-hidden">
                <img src="/Images/branding/logo.png" alt="WebMun logo" className="h-full w-auto object-contain" />
                <h1>Conselho de Segurança</h1>
                <Separator orientation="vertical" />
                <Timer />

                <div className="ml-auto flex shrink-0 items-center gap-3 pl-2">
                    <div className="flex flex-col items-end gap-1">
                        <h3 className="text-sm">
                            Topico discutido: <span className="font-semibold">
                                {currentTopicLabel}
                            </span>
                        </h3>
                        <Button variant="outline" size="sm" onClick={() => setIsAgendaOpen(true)}>Ver agenda</Button>
                    </div>
                    <Separator orientation="vertical" />
                    <div className="flex flex-col items-end text-right leading-tight">
                        <p className="text-sm font-semibold">Joao Silva</p>
                        <p className="text-xs text-muted-foreground">Mesa • Conselho de Segurança</p>
                    </div>
                    <Avatar className="h-9 w-9">
                        <AvatarImage src="/avatar.png" alt="Joao Silva" />
                        <AvatarFallback>JS</AvatarFallback>
                    </Avatar>
                </div>

            </div>

        </div>

        <Dialog open={isAgendaOpen} onOpenChange={setIsAgendaOpen}>
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
                                        <Button variant="outline" size="sm">
                                            <CircleCheckBig className="h-4 w-4" />
                                        </Button>
                                        <Button variant="destructive" size="sm">
                                            <Trash2 className="h-4 w-4" />
                                        </Button>

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
    </>)
}