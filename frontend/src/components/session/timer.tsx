import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Flag, Pause, Plus, Play } from "lucide-react"
import Flags from "@/components/ui/flags"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { sendMessage } from "@/pages/Session"
import { type IncreaseTimerEvent, type ToggleTimerEvent, ChairEvents } from "@/schemas/types.gen"
import { useEffect, useState } from "react"


export default function Timer() {


    const currentSpeaker = useCommitteeStore((state) => state.current_speaker);
    const speaker = currentSpeaker ?? {
        id: -1,
        seat: "",
        name: "Mesa",
        code: "null",
    };
    const timerIsRunning = useCommitteeStore((state) => state.timer_is_running) ?? false;
    const timerExpiration = useCommitteeStore((state) => state.timer_expiration);
    const timerRemaining = useCommitteeStore((state) => state.timer_remaining_seconds);
    const expirationDate = new Date(timerExpiration ?? "");

    const [remainingSeconds,setRemainingSeconds] = useState(0);

    useEffect(()=>{

        if(!timerIsRunning) 
        {
            setRemainingSeconds(timerRemaining ?? 0);
            return;
        }

        const interval = setInterval(() => {
            const finishtime = new Date(expirationDate).getTime();
            const now = new Date().getTime();
            setRemainingSeconds(Math.floor((finishtime - now)/1000))
        }, 1000);

        return ()=>{clearInterval(interval);}
    }, [expirationDate])

    return (<div className="flex h-full max-h-full items-center gap-2 rounded-md border-2 p-2">
        <div className="flex flex-col">
            <div className="flex items-center gap-2">
                <Flag />
                <h3 className="text-[1.5vh]">Orador com a Palavra:</h3>
            </div>
            <div className="flex items-center justify-center gap-2">
                <Flags code={speaker.code} className="h-5" />
                <h3 className="uppercase text-[1.75vh]">{speaker.name}</h3>
            </div>
        </div>
        <Separator orientation="vertical" />
        <div className="flex items-center gap-2">
            <h2 className="text-3xl leading-none font-bold tabular-nums">{Math.floor(remainingSeconds / 60).toString().padStart(2, '0')}:{(remainingSeconds % 60).toString().padStart(2, '0')}</h2>
            <Button variant="outline" size="icon-lg" aria-label={timerIsRunning ? "Pause timer" : "Start timer"} onClick={() => sendMessage({type: ChairEvents.TOGGLE_TIMER_EVENT, payload: {}} as ToggleTimerEvent)}>
                {timerIsRunning ? <Pause /> : <Play />}
            </Button>
            <Button onClick={() => sendMessage({type: ChairEvents.INCREASE_TIMER_EVENT, payload: { seconds: 5 }} as IncreaseTimerEvent)}><Plus />5s</Button>

        </div>

    </div>)
}