import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ScrollArea, } from "@/components/ui/scroll-area"
import {
    Item,
    ItemContent,
    ItemDescription,
    ItemFooter,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import { Badge } from "@/components/ui/badge"
export default function MotionsList() {

    return (<div className="m-4">
        <div className="flex items-center">
            <h2 className="text-xl font-bold">Moçoes Apresentadas</h2>
            <Badge className="ml-auto bg-tertiary-200 text-secondary"> 03 na fila</Badge>
        </div>
        <ScrollArea className="h-60 rounded-md border mt-4">
            <Item size="sm">
                <ItemMedia variant="icon" className=" h-10 w-10 bg-neutral-200 rounded-full">
                    <div className="h-10 items-center justify-center flex">
                        <h2 className="font-bold text-black text-xs">15:58</h2>
                    </div>
                </ItemMedia>
                <ItemContent>
                    <ItemTitle>Moção para debate moderado, de 3 discursos
                    </ItemTitle>
                    <ItemDescription>Republica Francesa</ItemDescription>
                </ItemContent>
                <ItemFooter className="flex-col items-stretch gap-2 pt-2">
                    <div className="flex items-center gap-2">
                        <Button size="sm" className="flex-1 bg-green-800 text-white hover:bg-green-700">Acatar</Button>
                        <Button size="sm" className="flex-1 bg-red-800 text-white hover:bg-red-700">Rejeitar</Button>
                    </div>
                    <Separator />
                </ItemFooter>
            </Item>
        </ScrollArea>
        <Separator></Separator>
    </div>)
}