import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { sendMessage } from "@/pages/Session"
import {
    Item,
    ItemContent,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import { CircleFlag } from 'react-circle-flags'
import { type MarkRollCallBulkEvent, ChairEvents, RollCallChoice } from "@/schemas/types.gen"


export default function ManualQuorum() {
    const delegations = useCommitteeStore((state) => state.delegations ?? [])
    const sortedDelegations = [...delegations].sort((a, b) =>
        a.name.localeCompare(b.name, "pt-BR", { sensitivity: "base" })
    )
    const currentQuorum = useCommitteeStore((state) => state.roll_call.registry ?? {})
    const tempQuorum = structuredClone(currentQuorum)


    return (
        <Dialog>
            <form>
                <DialogTrigger asChild>
                    <Button variant="outline" >
                        Editar Quórum
                    </Button>
                </DialogTrigger>
                <DialogContent className="">
                    <DialogHeader>
                        <DialogTitle>Quórum</DialogTitle>

                    </DialogHeader>
                    <ScrollArea className="mt-4 min-h-0 max-h-[75vh] flex-1 rounded-md border">
                        {sortedDelegations.map((delegation) => (
                            <Item key={delegation.id} size="sm">
                                <ItemMedia variant="image" >
                                    <CircleFlag countryCode={delegation.code} className="h-10 w-15" />
                                </ItemMedia>
                                <ItemContent className="flex-row items-center justify-between gap-4">
                                    <ItemTitle>{delegation.name}</ItemTitle>
                                    <ToggleGroup type="single" onValueChange={(value: RollCallChoice) => tempQuorum[delegation.id] = value} defaultValue={currentQuorum[delegation.id]} className="bg-neutral-200">
                                        <ToggleGroupItem value={RollCallChoice.PRESENT_AND_VOTING} className="hover:bg-green-700 hover:text-white data-[state=on]:bg-green-800 data-[state=on]:text-white">PV</ToggleGroupItem>
                                        <ToggleGroupItem value={RollCallChoice.PRESENT} className="hover:bg-green-700 hover:text-white data-[state=on]:bg-green-800 data-[state=on]:text-white">P</ToggleGroupItem>
                                        <ToggleGroupItem value={RollCallChoice.ABSENT} className="hover:bg-red-700 hover:text-white data-[state=on]:bg-red-800 data-[state=on]:text-white">Ausente</ToggleGroupItem>
                                    </ToggleGroup>
                                </ItemContent>
                            </Item>
                        ))}
                    </ScrollArea>
                    <DialogFooter>
                        <DialogClose asChild>
                            <Button type="submit" className="bg-green-800 text-white hover:bg-green-700" onClick={() => {
                                sendMessage({ type: ChairEvents.MARK_ROLL_CALL_BULK_EVENT, payload: { Rollcalls: tempQuorum } } as MarkRollCallBulkEvent)
                            }}>
                                Aceitar e Salvar Quorum
                            </Button>
                        </DialogClose>

                    </DialogFooter>
                </DialogContent>
            </form>
        </Dialog >
    )
}