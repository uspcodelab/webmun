import VoteButton from "./bottom-bar-buttons/VoteButton"
import MotionsButton from "./bottom-bar-buttons/MotionsButton"
import SpeechesButton from "./bottom-bar-buttons/SpeechesButton"
import HistoryButton from "./bottom-bar-buttons/HistoryButton"
import SessionButton from "./bottom-bar-buttons/SessionButton"
import ExitButton from "./bottom-bar-buttons/ExitButton"
import BRBButton from "./bottom-bar-buttons/BRB"


export default function BottomBar() {
    

    return (
        <>


            <div className="fixed bottom-0 left-0 z-30 flex h-[8vh] w-full items-center justify-center outline-2 outline-tertiary-100 bg-white">

                <ExitButton />
                <VoteButton />
                <MotionsButton />
                <SpeechesButton />
                <HistoryButton />
                <SessionButton />
                <BRBButton />

            </div>

        </>
    )
}