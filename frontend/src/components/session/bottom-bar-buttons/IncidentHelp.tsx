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


export default function TestButton() {
    return (
        <Dialog>
            <form>
                <DialogTrigger asChild>
                    <Button className="m-4 flex h-8/10 flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
                        <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
                            <TriangleAlert className="size-[3vh]" />
                        </span>
                        <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">INCIDENTES E AJUDA</h3>
                    </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-sm">
                    <DialogHeader>
                        <DialogTitle>Incidentes e Ajuda</DialogTitle>
                        <DialogDescription>Reportar incidentes e pedir ajuda externa</DialogDescription>
                    </DialogHeader>
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
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                        <Textarea className="mt-2 min-h-28 " placeholder="Descrição do Incidente" />
                        <Button className="mt-4">Enviar Incidente</Button>
                        <Separator className="my-4" />
                        <p className="font-bold">Pedir ajuda</p>
                        <p>Peça assistencia do secretariado ou orientadores</p>
                        <Button className="mt-2">Registrar chamado de ajuda não urgente</Button>
                        <Button className="mt-2">Registrar chamado de ajuda urgente</Button>
                        <Button className="mt-2"> Cancelar chamados</Button>
                        <p className="font-bold mt-2">Você não tem chamados abertos</p>


                    </div>
                </DialogContent>
            </form>
        </Dialog >
    )
}