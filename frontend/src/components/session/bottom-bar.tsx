import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
} from "@/components/ui/dialog"
import { useState } from "react"
import VoteButton, { VoteMenu } from "./bottom-bar-buttons/VoteButton"
import MotionsButton, { MotionsMenu } from "./bottom-bar-buttons/MotionsButton"
import SpeechesButton, { SpeechesMenu } from "./bottom-bar-buttons/SpeechesButton"
import HistoryButton, { HistoryMenu } from "./bottom-bar-buttons/HistoryButton"
import SessionButton, { SessionMenu } from "./bottom-bar-buttons/SessionButton"

export default function BottomBar() {
    const [openMenu, setOpenMenu] = useState<"vote" | "motions" | "speeches" | "history" | "session" | null>(null)
    const [MorQ, setMotionKind] = useState<"moção" | "questão">("moção")
    const [selectedMotion, setSelectedMotion] = useState<string>("")
    const [debateKindChange, setDebateKind] = useState<"moderado" | "não moderado" | "lista de discursos" | "">("")
    const [unmoderatedMinutes, setUnmoderatedMinutes] = useState("")
    const [speechCount, setSpeechCount] = useState("")
    const [minutesPerSpeech, setMinutesPerSpeech] = useState("")
    const [unlimitedDiscourses, setUnlimitedDiscourses] = useState(false)
    const [questionText, setQuestionText] = useState("")
    const [answerText, setAnswerText] = useState("")

    const menuContent = {
        vote: <VoteMenu />,
        motions: (
            <MotionsMenu
                motionKind={MorQ}
                setMotionKind={setMotionKind}
                selectedMotion={selectedMotion}
                setSelectedMotion={setSelectedMotion}
                debateKindChange={debateKindChange}
                setDebateKind={setDebateKind}
                unmoderatedMinutes={unmoderatedMinutes}
                setUnmoderatedMinutes={setUnmoderatedMinutes}
                speechCount={speechCount}
                setSpeechCount={setSpeechCount}
                minutesPerSpeech={minutesPerSpeech}
                setMinutesPerSpeech={setMinutesPerSpeech}
                unlimitedDiscourses={unlimitedDiscourses}
                setUnlimitedDiscourses={setUnlimitedDiscourses}
                questionText={questionText}
                setQuestionText={setQuestionText}
                answerText={answerText}
                setAnswerText={setAnswerText}
            />
        ),
        speeches: <SpeechesMenu />,
        history: <HistoryMenu />,
        session: <SessionMenu />,
    }[openMenu ?? "vote"]

    return (
        <>
            <div className="fixed bottom-0 left-0 z-20 flex h-[8vh] w-full items-center justify-center outline-2 outline-tertiary-100">
                <VoteButton onClick={() => setOpenMenu("vote")} />
                <MotionsButton onClick={() => setOpenMenu("motions")} />
                <SpeechesButton onClick={() => setOpenMenu("speeches")} />
                <HistoryButton onClick={() => setOpenMenu("history")} />
                <SessionButton onClick={() => setOpenMenu("session")} />

            </div>

            <Dialog open={openMenu !== null} onOpenChange={(isOpen) => !isOpen && setOpenMenu(null)}>
                <DialogContent>
                    {menuContent}

                    <DialogFooter className="items-start justify-start sm:justify-start">
                        <DialogClose asChild>
                            <Button>Fechar</Button>
                        </DialogClose>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </>
    )
}