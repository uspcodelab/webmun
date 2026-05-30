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

export type Speaker = {
    id: string
    position: number
    countryName: string
    countryCode: string
    speechTime: string
    isSpeaking?: boolean
}

type SpeakerListProps = {
    speakers: Speaker[]
}

export default function SpeakerList({ speakers }: SpeakerListProps) {
    const sortedSpeakers = [...speakers].sort((a, b) => a.position - b.position)
    const waitingCount = sortedSpeakers.length

    return (<div>
        <div className="flex items-center m-4">
            <h2 className="text-xl font-bold">Lista de Oradores</h2>
            <Badge className="ml-auto bg-tertiary-200 text-secondary">{String(waitingCount).padStart(2, "0")} em espera</Badge>
        </div>
        <ScrollArea className="pt-2 h-60 rounded-md border m-4">
            {sortedSpeakers.map((speaker) => (
                <Item size="sm" key={speaker.id}>
                    <ItemMedia
                        variant="icon"
                        className={`${speaker.isSpeaking ? "bg-secondary" : "bg-neutral-100"} h-10 w-10 rounded-full`}
                    >
                        <div className="h-10 items-center justify-center flex">
                            <h2 className={`font-bold text-lg ${speaker.isSpeaking ? "text-white" : "text-secondary"}`}>
                                {String(speaker.position).padStart(2, "0")}
                            </h2>
                        </div>
                    </ItemMedia>
                    <ItemContent>
                        <ItemTitle>
                            {speaker.countryName}
                            <Flags code={speaker.countryCode} className="h-5" />
                        </ItemTitle>
                        <ItemDescription>
                            {speaker.isSpeaking ? "Falando" : "Tempo de discurso"}: {speaker.speechTime}
                        </ItemDescription>
                    </ItemContent>
                    <ItemFooter>
                        <Separator></Separator>
                    </ItemFooter>
                </Item>
            ))}
        </ScrollArea>
        <Button variant="outline" className="mr-4 ml-4 mb-4 w-[calc(100%-2rem)]">
            Editar Lista
        </Button>
        <Separator></Separator>
    </div>)
}