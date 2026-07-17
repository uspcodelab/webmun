import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Lectern } from "lucide-react"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { States } from "@/schemas/types.gen"
import { useCommitteeStore } from "@/store/useCommitteeStore"

export default function TestButton() {
  const currentState = useCommitteeStore((state) => state.current_state)

  return (
    <Dialog>
        <DialogTrigger asChild>
          <Button disabled={currentState === States.SETUP_ROOM || currentState === States.ROLL_CALL} className="m-4 flex h-8/10   flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
              <Lectern className="size-[3vh]" />
            </span>
            <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">DISCURSOS</h3>
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>Discursos</DialogTitle>
            <DialogDescription>Controle os discursos e a ordem de oradores.</DialogDescription>
          </DialogHeader>
          <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
            <FieldGroup>
              <Field>
                <FieldLabel>Mudar o Tempo de Discurso (segundos):</FieldLabel>
                <Input type="number" placeholder="Segundos por discurso" className="h-8 w-full rounded-md border pl-2" />
                <Button className="bg-secondary-800 text-white hover:bg-secondary-700">Mudar tempo de Discurso</Button>
              </Field>
              <Separator />
              <Field>
                <FieldLabel>Mudar o Tipo de Debate</FieldLabel>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o novo tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="lista de discursos">Lista de Discursos</SelectItem>
                      <SelectItem value="moderado">Debate moderado</SelectItem>
                      <SelectItem value="não moderado">Debate não moderado</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
                <Button className="bg-secondary-800 text-white hover:bg-secondary-700">Mudar Tipo de Debate</Button>
              </Field>
            </FieldGroup>
          </div>
        </DialogContent>
    </Dialog >
  )
}