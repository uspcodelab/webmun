import VoteButton from "./bottom-bar-buttons/VoteButton"
import MotionsButton from "./bottom-bar-buttons/MotionsButton"
import SpeechesButton from "./bottom-bar-buttons/SpeechesButton"
import HistoryButton from "./bottom-bar-buttons/HistoryButton"
import SessionButton from "./bottom-bar-buttons/SessionButton"
import ExitButton from "./bottom-bar-buttons/ExitButton"
import BRBButton from "./bottom-bar-buttons/BRB"
import IncidentHelp from "./bottom-bar-buttons/IncidentHelp"
import { useSession } from "@/context/SessionContext"
import { SessionRoles} from "@/schemas/types.gen"


export default function BottomBar() {
    
    const {role} = useSession()
    const isChair = role===SessionRoles.CHAIR

    return (
        <>


            <div className="fixed bottom-0 left-0 z-30 flex h-[8vh] w-full items-center justify-center outline-2 outline-tertiary-100 bg-white">

                <ExitButton />
                {isChair && <VoteButton />}
                <MotionsButton />
                {isChair && <SpeechesButton />}
                {/* 
                TODO: Add history button when the history feature is implemented
                <HistoryButton /> 
                */}
                {isChair && <SessionButton />}
                {/*
                TODO: Add BRB button when the BRB feature is implemented
                !isChair && <BRBButton />
                */}
                {/*
                TODO: Add incident help button when the incident help feature is implemented
                isChair && <IncidentHelp />
                */}
            </div>

        </>
    )
}