import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Flag, Pause, Plus,} from "lucide-react"
import Flags from "@/components/ui/flags"


export default function Timer() {

    return (<div className=" flex items-center gap-2 p-2 border-2 rounded-md">
        <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
                <Flag />
                <h3>Orador com a Palavra:</h3>
            </div>
            <div className="flex items-center justify-center gap-2">
                <Flags code="fr" className="h-5" />
                <h3 className="uppercase">França</h3>
            </div>
        </div>
        <Separator orientation="vertical" />
        <div className="flex items-center gap-2">
            <h2 className="text-3xl leading-none font-bold tabular-nums">01:53</h2>
            <Button variant="outline" size="icon-lg" aria-label="Pause timer">
                <Pause />
            </Button>
            <Button><Plus />5s</Button>

        </div>

    </div>)
}