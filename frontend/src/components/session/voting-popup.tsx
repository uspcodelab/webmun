import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import {
    Field,
    FieldContent,
    FieldDescription,
    FieldLabel,
} from "@/components/ui/field"
import { useState } from "react"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { sendMessage, useSession } from "@/context/SessionContext"
import { DelegateEvents, SessionRoles, VotingChoice, type CastVoteEvent } from "@/schemas/types.gen"

type VoteType = "rollCall1" | "rollCall2" | "procedural" | "informal"

const canAbstain = false

const voteType : VoteType = "procedural"

export default function VotingPopup() {

    const {role, representation_id} = useSession()
    const isChair = role == SessionRoles.CHAIR

    //TODO: Implement rollcall voting
    const isRollCall1 = voteType === "rollCall1"
    const isRollCall2 = voteType === "rollCall2"
    const isRollCall = isRollCall1 || isRollCall2
    const [voteWithRights, setVoteWithRights] = useState(false)
    //TEMPORARY^^^^

    const voting = useCommitteeStore((state) => state.voting ?? null)
    const voted = voting && representation_id ? representation_id in voting.voting_registry! : true
    const voteTitle = voting?.title
    const [clicked, setClicked] = useState(false)

    return (
        <Dialog  open={!isChair && voting !== null && !clicked && !voted}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Votação</DialogTitle>
                    <DialogDescription>{voteTitle}</DialogDescription>
                </DialogHeader>
                {isRollCall && (
                    <div className="rounded-xl border bg-muted/30 p-4 text-sm text-muted-foreground">
                        {isRollCall1
                            ? "Primeira rodada: Sua delegação pode votar com ou sem direitos. Caso deseje pular, podera votar apos todos, porem sem a possibilidade de pedir direitos"
                            : "Segunda rodada: apenas satisfies delegações que pularam na primeira rodada podem votar, sem direitos."}
                    </div>
                )}

                {isRollCall1 && (
                    <Field orientation="horizontal" className="rounded-xl border bg-muted/30 p-4 text-sm ">
                        <Checkbox
                            id="vote-with-rights"
                            checked={voteWithRights}
                            onCheckedChange={(checked) =>
                                setVoteWithRights(checked === true)
                            }
                        />
                        <FieldContent>
                            <FieldLabel className="hover:cursor-pointer" htmlFor="vote-with-rights">
                                Votar com direitos
                            </FieldLabel>
                            <FieldDescription>
                                Ao votar com direitos, você terá direito a uma fala curta para justificar por que votou contra suas convicções do debate.
                            </FieldDescription>
                        </FieldContent>
                    </Field>

                )}

                <DialogFooter className="flex gap-4 margin-auto">
                    <div className="flex w-full flex-row gap-2">
                        <Button onClick={
                            () => {setClicked(true); sendMessage({type:DelegateEvents.CAST_VOTE_EVENT, payload: {vote:VotingChoice.FAVOUR}} satisfies CastVoteEvent)}}
                             className="flex-1 bg-green-800 text-white hover:bg-green-700">A Favor</Button>
                        <Button
                            onClick={
                            () => {setClicked(true); sendMessage({type:DelegateEvents.CAST_VOTE_EVENT, payload: {vote:VotingChoice.FAVOUR}} satisfies CastVoteEvent)}}
                            disabled={isRollCall && !canAbstain}
                            className="flex-1 bg-gray-700 text-white hover:bg-gray-600 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            Abstenção
                        </Button>
                        {isRollCall1 && (
                            <Button className="flex-1 bg-gray-700 text-white hover:bg-gray-600" >
                                Pular
                            </Button>
                        )}
                        <Button onClick={() => {setClicked(true); sendMessage({type:DelegateEvents.CAST_VOTE_EVENT, payload: {vote:VotingChoice.FAVOUR}} satisfies CastVoteEvent)}}
                        className="flex-1 bg-red-800 text-white hover:bg-red-700">Contra</Button>

                    </div>


                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}