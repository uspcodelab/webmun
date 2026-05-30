import { ScrollText } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"

type HistoryButtonProps = {
    onClick: () => void
}

export default function HistoryButton({ onClick }: HistoryButtonProps) {
    return (
        <Button
            onClick={onClick}
            className="m-4 flex h-8/10 flex-col items-center justify-center bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <ScrollText className="size-[3vh]" />
            <h3 className="text-xs">HISTÓRICO DA SESSÃO</h3>
        </Button>
    )
}

export function HistoryMenu() {
    return (
        <div className="grid gap-2">
            <DialogHeader>
                <DialogTitle>Histórico da sessão</DialogTitle>
                <DialogDescription>Veja os eventos recentes da sessão.</DialogDescription>
            </DialogHeader>
            <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
                Placeholder: Sessão menu (implement unique UI here)
            </div>
        </div>
    )
}