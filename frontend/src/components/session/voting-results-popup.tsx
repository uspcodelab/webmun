import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogClose,
} from "@/components/ui/dialog"

import { useCommitteeStore } from "@/store/useCommitteeStore"
import { MajorityTypes, VotingChoice, RollCallChoice } from "@/schemas/types.gen"
import { Button } from "@/components/ui/button"
import { useState } from "react"



export default function VotingResultsPopup() {



    const voting = useCommitteeStore((state) => state.voting ?? null)
    const voteTitle = voting?.title ?? voting?.motion_in_vote?.type ?? "ERROR:VotingTitle not found"

    const expectedVotes = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice !== RollCallChoice.ABSENT).length)
    const yayVotes = useCommitteeStore((state) => Object.entries(state.voting?.voting_registry ?? {}).filter(([, choice]) => choice === VotingChoice.FAVOUR).length)
    const nayVotes = useCommitteeStore((state) => Object.entries(state.voting?.voting_registry ?? {}).filter(([, choice]) => choice === VotingChoice.AGAINST).length)
    const abstentions = expectedVotes - yayVotes - nayVotes
    const yayPercentage = expectedVotes > 0 ? (yayVotes / expectedVotes) * 100 : 0
    const nayPercentage = expectedVotes > 0 ? (nayVotes / expectedVotes) * 100 : 0
    const majorityType = useCommitteeStore((state) => state.voting?.majority ?? MajorityTypes.MAIORIA_SIMPLES)
    const requiredMajority = majorityType === MajorityTypes.MAIORIA_QUALIFICADA
        ? Math.ceil(expectedVotes * 2 / 3)
        : majorityType === MajorityTypes.CONSENSO
            ? expectedVotes
            : Math.floor(expectedVotes / 2) + 1
    const requiredMajorityPercentage = expectedVotes > 0 ? (requiredMajority / expectedVotes) * 100 : 0
    const requiredMajorityAngle = Math.PI * requiredMajorityPercentage / 100
    const markerInnerRadius = 67
    const markerOuterRadius = 94
    const markerStartX = 100 - markerInnerRadius * Math.cos(requiredMajorityAngle)
    const markerStartY = 100 - markerInnerRadius * Math.sin(requiredMajorityAngle)
    const markerEndX = 100 - markerOuterRadius * Math.cos(requiredMajorityAngle)
    const markerEndY = 100 - markerOuterRadius * Math.sin(requiredMajorityAngle)

    const canBeVetoed = useCommitteeStore((state) => state.voting?.allow_veto_power ?? false)
    const delegations = useCommitteeStore((state) => state.delegations)
    const whoCanVeto = Object.values(delegations)
        .filter((delegation) => ["fr", "us", "cn", "ru", "uk"].includes(delegation.code?.toLowerCase() ?? ""))
        .map((delegation) => delegation.id)
    const isVetoed = useCommitteeStore((state) => {
        const votingRegistry = state.voting?.voting_registry
        if (!votingRegistry) return false

        return Object.entries(votingRegistry)
            .some(([id, choice]) => choice === VotingChoice.AGAINST
                && whoCanVeto.some((vetoId) => String(vetoId) === id))
    })

    const [open, setOpen] = useState(true)


    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Resultados da Votação</DialogTitle>
                    <DialogDescription>{voteTitle}</DialogDescription>
                </DialogHeader>
                <div className="flex flex-col items-center gap-4 py-4">
                    <div className="relative w-full max-w-sm">
                        <svg
                            viewBox="0 0 200 110"
                            className="h-auto w-full"
                            role="img"
                            aria-label={`${yayVotes} de ${expectedVotes} votos a favor`}
                        >
                            <path
                                d="M 20 100 A 80 80 0 0 1 180 100"
                                pathLength="100"
                                fill="none"
                                stroke="#d4d4d4"
                                strokeWidth="20"
                            />
                            <path
                                d="M 20 100 A 80 80 0 0 1 180 100"
                                pathLength="100"
                                fill="none"
                                stroke="#15803d"
                                strokeWidth="20"
                                strokeDasharray={`${yayPercentage} ${100 - yayPercentage}`}
                            />
                            <path
                                d="M 20 100 A 80 80 0 0 1 180 100"
                                pathLength="100"
                                fill="none"
                                stroke="#b91c1c"
                                strokeWidth="20"
                                strokeDasharray={`${nayPercentage} ${100 - nayPercentage}`}
                                strokeDashoffset={-yayPercentage}
                            />
                            <line
                                x1={markerStartX}
                                y1={markerStartY}
                                x2={markerEndX}
                                y2={markerEndY}
                                stroke="#171717"
                                strokeWidth="2"
                                strokeLinecap="round"
                            >
                                <title>{`Maioria necessária: ${requiredMajority} de ${expectedVotes}`}</title>
                            </line>
                            <text x="100" y="82" textAnchor="middle" className="fill-neutral-900 text-[9px] font-bold">
                                {yayVotes}/{expectedVotes} a favor
                            </text>
                        </svg>
                    </div>
                    <div className="flex flex-wrap justify-center gap-x-5 gap-y-2 text-sm">
                        <span className="flex items-center gap-2">
                            <span className="size-3 rounded-full bg-green-700" />
                            A favor: {yayVotes}
                        </span>
                        <span className="flex items-center gap-2">
                            <span className="size-3 rounded-full bg-red-700" />
                            Contra: {nayVotes}
                        </span>
                        <span className="flex items-center gap-2">
                            <span className="size-3 rounded-full bg-neutral-300" />
                            Abstenções: {Math.max(abstentions, 0)}
                        </span>
                    </div>
                    {canBeVetoed && isVetoed && (
                        <h2 className="text-red-700 font-bold text-xl">A moção foi vetada.</h2>
                    )}
                    {!canBeVetoed || !isVetoed ? yayVotes >= requiredMajority ? (
                        <h2 className="text-green-700 font-bold text-xl">A moção passa!</h2>
                    ) : (
                        <h2 className="text-red-700 font-bold text-xl">A moção nao passsa.</h2>
                    ) : null}

                </div>


                <DialogFooter className="flex gap-4 margin-auto">
                    <DialogClose asChild>
                        <Button variant="outline">Fechar</Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}