import { Cog } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"

type SessionButtonProps = {
    onClick: () => void
}

export default function SessionButton({ onClick }: SessionButtonProps) {
    return (
        <Button
            onClick={onClick}
            className="m-4 flex h-8/10 flex-col items-center justify-center bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <Cog className="size-[3vh]" />
            <h3 className="text-xs">SESSAO</h3>
        </Button>
    )
}

export function SessionMenu() {
    return (
        <div className="grid gap-2">
            <DialogHeader>
                <DialogTitle>Sessao</DialogTitle>
                <DialogDescription>Configure e acompanhe o estado da sessao.</DialogDescription>
            </DialogHeader>
            <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
                Placeholder: Sessão menu (implement unique UI here)
            </div>
        </div>
    )
}