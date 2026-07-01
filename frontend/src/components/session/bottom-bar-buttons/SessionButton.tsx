import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Cog } from "lucide-react"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import ManualQuorum from "@/components/session/manual-quorum"
import { RollCallChoice, ChairEvents, type CloseRollCallEvent } from "@/schemas/types.gen"
import { sendMessage } from "@/pages/Session"
import { useCommitteeStore } from "@/store/useCommitteeStore"


export default function TestButton() {
  const presentDelegations = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice !== RollCallChoice.ABSENT).length)
  const delegations = useCommitteeStore((state) => state.delegations.length ?? 0)

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
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>Sessao</DialogTitle>
            <DialogDescription>Configure e acompanhe o estado da sessao.</DialogDescription>
          </DialogHeader>
          <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
            <p>A sessão está: Aberta/Fehada</p>
            <Button>Abrir/Fechar Sessão</Button>
            <Separator className="my-4" />
            <div className="gap-2 flex flex-col">
              <p>Quorum Atual: {presentDelegations}/{delegations}</p>
              <ManualQuorum />
              <div className="inline-flex gap-2">
                <Button variant="outline" className="bg-green-800 text-white hover:bg-green-700" disabled>Abrir Quórum</Button>
                <Button variant="destructive" className="bg-red-800 text-white hover:bg-red-700" onClick={() => sendMessage({type: ChairEvents.CLOSE_ROLL_CALL_EVENT, payload: {}} as CloseRollCallEvent)}>
                  Fechar Quórum
                </Button>
              </div>
            </div>
            <Separator className="my-4" />
            <p>Suspensão de sessão</p>
            <Button>Suspender Sessão</Button>
            <Separator className="my-4" />
            <p>Estado do comitê: Debate</p>
            <Select>
              <SelectTrigger className="w-full max-w-48">
                <SelectValue placeholder="Selecione um estado do comitê" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Selecione um estado do comitê</SelectLabel>
                  <SelectItem value="agenda">Agenda</SelectItem>
                  <SelectItem value="debate">Debate</SelectItem>
                  <SelectItem value="crise">Crise</SelectItem>
                  <SelectItem value="suspensao">Suspensão</SelectItem>
                  <SelectItem value="votacao">Votação</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Button className="mt-4">Mudar Estado do Comitê</Button>
          </div>
        </DialogContent>
      </form>
    </Dialog >
  )
}
