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
import { RollCallChoice, ChairEvents, States, type CloseRollCallEvent, type CloseSessionEvent } from "@/schemas/types.gen"
import { sendMessage } from "@/pages/Session"
import { useCommitteeStore } from "@/store/useCommitteeStore"


export default function TestButton() {
  const presentDelegations = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([_, choice]) => choice !== RollCallChoice.ABSENT).length)
  const delegations = useCommitteeStore((state) => state.delegations.length ?? 0)
  const currentState = useCommitteeStore((state) => state.current_state)

  return (
    <Dialog>

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
          <DialogDescription>Mude e acompanhe o estado da sessao.</DialogDescription>
        </DialogHeader>
        <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
          <p className="mb-2 font-bold">Quorum</p>
          <p className="mb-2">Quorum Atual: {presentDelegations}/{delegations}</p>
          <ManualQuorum />
          <div className="flex flex-row gap-2 mt-4">
            {currentState === States.SETUP_ROOM &&
              <Button variant="outline" className="bg-green-800 text-white hover:bg-green-700" disabled>Abrir Sessao e iniciar Quórum</Button>}
            {currentState === States.ROLL_CALL &&
              <Button variant="destructive" onClick={() => sendMessage({ type: ChairEvents.CLOSE_ROLL_CALL_EVENT, payload: {} } as CloseRollCallEvent)}>
                Fechar Quórum
              </Button>}
            {currentState !== States.SETUP_ROOM && currentState !== States.ROLL_CALL &&
              <Button variant="destructive" className="bg-red-800 text-white hover:bg-red-700" onClick={() => sendMessage({ type: ChairEvents.CLOSE_SESSION_EVENT, payload: {} } as CloseSessionEvent)}>
                Fechar Sessão
              </Button>}
          </div>
          <Separator className="my-4" />
          <p>Suspensão de sessão</p>
          <Button className="mt-2 font-bold">Suspender Sessão</Button>
          <Separator className="my-4" />
          <p className="mb-2 font-bold">Estado do Comitê</p>
          <p>Estado atual do comitê: {String(currentState)}</p>
          <Select>
            <SelectTrigger className="w-full mt-2">
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
          <Button className="mt-2">Mudar Estado do Comitê</Button>
        </div>
      </DialogContent>
    </Dialog >
  )
}