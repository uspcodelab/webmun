import { Vote } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from "@/components/ui/dialog"

type VoteButtonProps = {
    onClick: () => void
}

export default function VoteButton({ onClick }: VoteButtonProps) {
    return (
        <Button
            onClick={onClick}
            className="m-4 flex h-8/10 flex-col items-center justify-center bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <Vote className="size-[3vh]" />
            <h3 className="text-xs">VOTACAO</h3>
        </Button>
    )
}

export function VoteMenu() {
    return (
        <div className="grid gap-2">
            <DialogHeader>
                <DialogTitle>Votacao</DialogTitle>
                <DialogDescription>Inicie uma votação informal</DialogDescription>
            </DialogHeader>
            <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
                <div className="grid gap-4">
                    <div className="grid gap-2">
                        <label className="text-sm font-medium">Título da Votação</label>
                        <input className="h-9 rounded-md border px-3" placeholder="Estamos de acordo com o paragrafo X?" />
                        <p className="text-xs text-muted-foreground">O que vai ser votado</p>
                    </div>
                    <div className="grid gap-2">
                        <label className="text-sm font-medium">Maioria necessária:</label>
                        <select className="h-9 rounded-md border px-3">
                            <option>Maioria Simples</option>
                            <option>Maioria Qualificada</option>
                            <option>Consenso</option>
                        </select>
                    </div>
                    <div className="flex items-start gap-3">
                        <input type="checkbox" className="mt-1" defaultChecked />
                        <div className="grid gap-1">
                            <label className="text-sm font-medium">P5 tem poder de veto nesta votacao?</label>
                            <p className="text-xs text-muted-foreground">
                                Os membros permanentes do conselho de seguranca podem exprimir que vetarão a proposição na votação final da proposta.
                            </p>
                        </div>
                    </div>
                    <Button className="w-full bg-green-800 text-white hover:bg-green-700">Iniciar Votação</Button>
                </div>
            </div>
        </div>
    )
}