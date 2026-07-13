import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { TriangleAlert } from "lucide-react"
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
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Checkbox } from "@/components/ui/checkbox"
import {
    Field,
    FieldContent,
    FieldDescription,
    FieldLabel,
} from "@/components/ui/field"

export default function TestButton() {
    return (
        <Dialog>

            <DialogTrigger asChild>
                <Button className="m-4 flex h-8/10 flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
                    <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
                        <TriangleAlert className="size-[3vh]" />
                    </span>
                    <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">INCIDENTES E AJUDA</h3>
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md  max-h-[90vh] flex-col overflow-hidden">
                <DialogHeader>
                    <DialogTitle>Incidentes e Ajuda</DialogTitle>
                    <DialogDescription>Reportar incidentes e pedir ajuda externa</DialogDescription>
                </DialogHeader>
                <ScrollArea className="min-h-0 flex-1 max-h-[70vh]">
                    <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
                        <p className="font-bold">Reportar Incidente</p>
                        <p>Atenção: Ao reportar un incidente, esse será registrado no histórico da sessão e um aviso sera enviado ao secretariado.</p>
                        <Select>
                            <SelectTrigger className="w-full mt-2">
                                <SelectValue placeholder="Selecione um Incidente" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <SelectLabel>Selecione um Incidente</SelectLabel>
                                    <SelectItem value="agenda">Falta de decoro leve</SelectItem>
                                    <SelectItem value="debate">Falta de decoro grave</SelectItem>
                                    <SelectItem value="suspensao">Falta de respeito a mesa</SelectItem>
                                    <SelectItem value="suspensao">Outro</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                        <Textarea className="mt-2 min-h-28 " placeholder="Descrição do Incidente" />
                        <Button className="mt-4">Enviar Incidente</Button>
                        <Separator className="my-4" />
                        <p className="font-bold">Pedir ajuda</p>
                        <p>Peça assistencia do secretariado, orientadores, apoio psicológico ou TI</p>
                        <p className="font-bold mt-2">OBS: Você não tem chamados abertos</p>
                        <Select>
                            <SelectTrigger className="w-full mt-2">
                                <SelectValue placeholder="Pedir ajuda para" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <SelectLabel>Pedir ajuda para</SelectLabel>
                                    <SelectItem value="agenda">Secretariado</SelectItem>
                                    <SelectItem value="debate">Orientadores</SelectItem>
                                    <SelectItem value="suspensao">Apoio Psicológico</SelectItem>
                                    <SelectItem value="suspensao">TI</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                        <Textarea className="mt-2 min-h-28 " placeholder="Descrição do Problema" />
                        <Field orientation="horizontal" className=" p-4 text-sm ">
                            <Checkbox id="urgent" />
                            <FieldContent>
                                <FieldLabel className="hover:cursor-pointer" htmlFor="urgent">
                                    Chamado Urgente
                                </FieldLabel>
                                <FieldDescription>
                                    Seu chamado será priorizado. use com responsabilidade e nunca para problemas pequenos.
                                </FieldDescription>
                            </FieldContent>
                        </Field>
                        <Button className="mt-4" variant="default">
                            Abrir Chamado
                        </Button>



                    </div>
                </ScrollArea>
            </DialogContent>
        </Dialog >
    )
}