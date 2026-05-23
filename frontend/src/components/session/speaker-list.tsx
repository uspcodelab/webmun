import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea,} from "@/components/ui/scroll-area"
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

export default function SpeakerList() {

    return (<div>
        <div className="flex items-center m-4">
            <h2 className="text-xl font-bold">Lista de Oradores</h2>
            <Badge className="ml-auto bg-tertiary-200 text-secondary"> 03 em espera</Badge>
        </div>
        <ScrollArea className="pt-2 h-60 rounded-md border m-4">
            <Item size="sm">
                <ItemMedia variant="icon" className="bg-secondary h-10 w-10 rounded-full">
                    <div className="h-10 items-center justify-center flex">
                        <h2 className="font-bold text-white text-lg">01</h2>
                    </div>
                </ItemMedia>
                <ItemContent>
                    <ItemTitle>França
                            <Flags code="fr" className="h-5" />
                    </ItemTitle>
                    <ItemDescription>Falando: 01:53</ItemDescription>
                </ItemContent>
                <ItemFooter><Separator></Separator></ItemFooter>
            </Item>
            <Item size="sm">
                <ItemMedia variant="icon" className="bg-neutral-100 h-10 w-10 rounded-full">
                    <div className="h-10 items-center justify-center flex">
                        <h2 className="font-bold text-secondary text-lg">02</h2>
                    </div>
                </ItemMedia>
                <ItemContent>
                    <ItemTitle>Brasil
                        <Flags code="br" className="h-5" />
                    </ItemTitle>
                    <ItemDescription>Tempo de discurso: 02:00</ItemDescription>
                </ItemContent>
                <ItemFooter><Separator></Separator></ItemFooter>
            </Item>
            <Item size="sm">
                <ItemMedia variant="icon" className="bg-neutral-100 h-10 w-10 rounded-full">
                    <div className="h-10 items-center justify-center flex">
                        <h2 className="font-bold text-secondary text-lg">03</h2>
                    </div>
                </ItemMedia>
                <ItemContent>
                    <ItemTitle>Brasil
                        <Flags code="br" className="h-5" />
                    </ItemTitle>
                    <ItemDescription>Tempo de discurso: 02:00</ItemDescription>
                </ItemContent>
                <ItemFooter><Separator></Separator></ItemFooter>
            </Item>
            <Item size="sm">
                <ItemMedia variant="icon" className="bg-neutral-100 h-10 w-10 rounded-full">
                    <div className="h-10 items-center justify-center flex">
                        <h2 className="font-bold text-secondary text-lg">04</h2>
                    </div>
                </ItemMedia>
                <ItemContent>
                    <ItemTitle>Brasil
                        <Flags code="br" className="h-5" />
                    </ItemTitle>
                    <ItemDescription>Tempo de discurso: 02:00</ItemDescription>
                </ItemContent>
                <ItemFooter><Separator></Separator></ItemFooter>
            </Item>
        </ScrollArea>
        <Button variant="outline" className="mr-4 ml-4 mb-4 w-[calc(100%-2rem)]">
            Editar Lista
        </Button>
        <Separator></Separator>
    </div>)
}