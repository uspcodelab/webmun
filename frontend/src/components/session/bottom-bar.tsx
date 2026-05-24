import { Button } from "@/components/ui/button"
import { Flag, Pause, Hand, Cog, Vote, Lectern } from "lucide-react"


export default function BottomBar() {

    return (<div className="fixed bottom-0 left-0 z-20 flex h-[8vh] w-full items-center justify-center outline-2 outline-tertiary-100">
        <Button className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <Vote className="size-[3vh]" />
            <h3 className="text-xs">VOTAÇÃO</h3>
        </Button>
        <Button className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <Hand className="size-[3vh]" />
            <h3 className="text-xs">QUESTÕES & MOÇÕES</h3>
        </Button>
        <Button className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <Lectern className="size-[3vh]" />
            <h3 className="text-xs">DISCURSOS</h3>
        </Button>
        <Button className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <Cog className="size-[3vh]" />
            <h3 className="text-xs">SESSÃO</h3>
        </Button>
        
    </div>)
}