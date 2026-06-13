import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Cog } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"

import {
    Item,
    ItemContent,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import Flags from "@/components/ui/flags"


export default function ManualQuorum() {
    const delegations = [
        { id: "fr", countryName: "França", countryCode: "fr" },
        { id: "br", countryName: "Brasil", countryCode: "br" },
        { id: "es", countryName: "Espanha", countryCode: "es" },
    ]


    return (
        <Dialog>
            <form>
                <DialogTrigger asChild>
                    <Button className="m-4 flex h-8/10 flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
                        <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
                            <Cog className="size-[3vh]" />
                        </span>
                        <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">SESSÃO</h3>
                    </Button>
                </DialogTrigger>
                <DialogContent className="">
                    <DialogHeader>
                        <DialogTitle>Quórum</DialogTitle>
                        
                    </DialogHeader>
                    <ScrollArea className="mt-4 min-h-0 flex-1 rounded-md border">
                        {delegations.map((delegation) => (
                            <Item key={delegation.id} size="sm">
                                <ItemMedia variant="image" className="bg-neutral-200">
                                    <Flags code={delegation.countryCode} className="h-10 w-15" />
                                </ItemMedia>
                                <ItemContent className="flex-row items-center justify-between gap-4">
                                    <ItemTitle>{delegation.countryName}</ItemTitle>
                                    <ToggleGroup type="single" className="bg-neutral-200">
                                        <ToggleGroupItem value="presentVoting" className="hover:bg-green-700 hover:text-white data-[state=on]:bg-green-800 data-[state=on]:text-white">PV</ToggleGroupItem>
                                        <ToggleGroupItem value="present" className="hover:bg-green-700 hover:text-white data-[state=on]:bg-green-800 data-[state=on]:text-white">P</ToggleGroupItem>
                                        <ToggleGroupItem value="absent" className="hover:bg-red-700 hover:text-white data-[state=on]:bg-red-800 data-[state=on]:text-white">Ausente</ToggleGroupItem>
                                    </ToggleGroup>
                                </ItemContent>
                            </Item>
                        ))}
                    </ScrollArea>
                </DialogContent>
            </form>
        </Dialog >
    )
}