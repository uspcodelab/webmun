import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "../ui/button"

export default function VotingPopup() {
    return (
        <Dialog>
            <DialogTrigger>Open</DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Votação</DialogTitle>
                    <DialogDescription>
                        Batata no Coffe Break
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter className="flex justify-center items-center gap-4">
                    <Button>A favor</Button>
                    <Button>Abstenção</Button>
                    <Button>Contra</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}