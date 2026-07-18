import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Play, Pause } from "lucide-react"
import { useState } from "react"



export default function UnmoderatedDebate() {
    const [isRunning, setIsRunning] = useState(false)


//TODO: Actually implement speaker history
    return (
        <div className="flex min-h-0 flex-1 flex-col">
            <div className="mr-4 mb-2 ml-4 mt-4 ">
                <h2 className="text-xl font-bold">Debate Não Moderado</h2>
            </div>

            <div className="flex flex-1 flex-col items-center justify-center gap-6 px-4">
                <div className="text-6xl font-bold tracking-tight text-secondary">08:00</div>
                <Button
                    type="button"
                    size="icon"
                    variant="outline"
                    onClick={() => setIsRunning((current) => !current)}
                >
                    {isRunning ? <Pause className="h-9 w-9" /> : <Play className="h-9 w-9" />}
                </Button>
                <p className="text-sm text-muted-foreground">Temporizador placeholder</p>
            </div>

            <Separator></Separator>

        </div>)
}