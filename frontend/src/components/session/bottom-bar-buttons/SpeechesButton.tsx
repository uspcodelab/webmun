import { Lectern } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
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

type SpeechesButtonProps = {
    onClick: () => void
}

export default function SpeechesButton({ onClick }: SpeechesButtonProps) {
    return (
        <Button
            onClick={onClick}
            className="m-4 flex h-8/10 flex-col items-center justify-center bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <Lectern className="size-[3vh]" />
            <h3 className="text-xs">DISCURSOS</h3>
        </Button>
    )
}

export function SpeechesMenu() {
    return (
        <div className="grid gap-2">
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
        </div>
    )
}