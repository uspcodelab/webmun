import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"

import { useCommitteeStore } from "@/store/useCommitteeStore"
import { Badge } from "@/components/ui/badge"

import { sendMessage, useSession } from "@/context/SessionContext"
import { SessionRoles, RollCallChoice, VotingChoice, MajorityTypes, type CloseInformalVotingEvent, VotingType, type CloseProceduralVotingEvent, ChairEvents } from "@/schemas/types.gen"

//TODO implement rules of procedure to determine if abstentions count towards the majority or not. For now, we will assume they do not count towards the majority.

export default function VotingMenu() {

    const voteTitle = useCommitteeStore((state) => state.voting?.title ?? state.voting?.motion_in_vote?.type ?? "ERROR:VotingTitle not found")
    const voting = useCommitteeStore((state) => state.voting ?? null)

    const expectedVotes = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice !== RollCallChoice.ABSENT).length)
    const yayVotes = Object.entries(voting?.voting_registry ?? {}).filter(([, choice]) => choice === VotingChoice.FAVOUR).length
    const nayVotes = Object.entries(voting?.voting_registry ?? {}).filter(([, choice]) => choice === VotingChoice.AGAINST).length
    const abstentions = Object.entries(voting?.voting_registry ?? {}).filter(([, choice]) => choice === VotingChoice.ABSTAIN).length
    const majorityType = voting?.majority ?? MajorityTypes.MAIORIA_SIMPLES
    const requiredMajority = majorityType === MajorityTypes.MAIORIA_QUALIFICADA
        ? Math.ceil(expectedVotes * 2 / 3)
        : majorityType === MajorityTypes.CONSENSO
            ? expectedVotes
            : Math.floor(expectedVotes / 2) + 1

    const canBeVetoed = voting?.allow_veto_power ?? false
    const delegations = useCommitteeStore((state) => state.delegations)
    const whoCanVeto = Object.values(delegations)
        .filter((delegation) => ["fr", "us", "cn", "ru", "uk"].includes(delegation.code?.toLowerCase() ?? ""))
        .map((delegation) => delegation.id)
    const isVetoed = voting?.voting_registry ? Object.entries(voting?.voting_registry)
            .some(([id, choice]) => choice === VotingChoice.AGAINST
                && whoCanVeto.some((vetoId) => String(vetoId) === id)) : false

    const { role } = useSession()
    const isChair = role === SessionRoles.CHAIR

    const votedCount = yayVotes + nayVotes + abstentions
    const pendingVotes = expectedVotes - votedCount
    const majorityPosition = expectedVotes
        ? Math.min(100, Math.max(0, (requiredMajority / expectedVotes) * 100))
        : 0


    return (
        <div className="flex min-h-0 flex-col">
            <div className="mr-4 mb-2 ml-4 mt-4 ">
                <h2 className="text-xl font-bold">Votação em progresso</h2>
                <p className="ml-auto text-muted-foreground">{voteTitle}</p>
            </div>
            <div className="mx-4">
                <p className="font-bold">Resultados parciais:</p>
                <p className="flex justify-center my-4">Votaram {votedCount} de {expectedVotes} delegações</p>


                <div className="mb-4 flex flex-col gap-2">
                    <div
                        className="relative h-8 w-full overflow-hidden rounded-full border bg-gray-100"
                        role="img"
                        aria-label={`Resultados: ${yayVotes} sim, ${nayVotes} nao, ${abstentions} abstencoes e ${pendingVotes} votos pendentes`}
                    >
                        <div className="absolute inset-0 flex">
                            <div
                                className="h-full bg-green-700"
                                style={{ width: `${(yayVotes / expectedVotes) * 100 || 0}%` }}
                            />
                            <div
                                className="h-full bg-red-700"
                                style={{ width: `${(nayVotes / expectedVotes) * 100 || 0}%` }}
                            />
                            <div
                                className="h-full bg-gray-500"
                                style={{ width: `${(abstentions / expectedVotes) * 100 || 0}%` }}
                            />
                            <div
                                className="h-full bg-gray-100"
                                style={{
                                    width: `${(pendingVotes / expectedVotes) * 100 || 0}%`,
                                    backgroundImage: "repeating-linear-gradient(135deg, transparent, transparent 6px, rgba(107, 114, 128, 0.22) 6px, rgba(107, 114, 128, 0.22) 10px)",
                                }}
                            />
                        </div>
                        <div
                            className="absolute inset-y-0 w-0.5 bg-black"
                            style={{ left: `${majorityPosition}%` }}
                        />
                    </div>

                </div>
                <div className="flex flex-row gap-2 justify-center my-4">
                    <Badge className="bg-green-200 text-green-800">Sim: {yayVotes}</Badge>
                    <Badge className="bg-gray-200 text-gray-800">Abstenção: {abstentions}</Badge>
                    <Badge className="bg-red-200 text-red-800">Não: {nayVotes}</Badge>
                </div>
                <p className="text-muted-foreground flex justify-center mb-4">Maioria Necessaria: {requiredMajority} votos</p>

            </div>
            <div className="flex justify-center items-center mb-4">
            {canBeVetoed && isVetoed && (
                <h2 className="text-red-700 font-bold text-xl">A moção foi vetada.</h2>
            )}
            {!canBeVetoed || !isVetoed ? yayVotes >= requiredMajority ? (
                <h2 className="text-green-700 font-bold text-xl">A moção passa!</h2>
            ) : (
                <h2 className="text-red-700 font-bold text-xl">A moção nao passsa.</h2>
            ) : null}
            </div>
            {isChair && (
                <div className="ml-4 mr-4 mb-2   flex w-auto min-w-0 flex-row gap-2 overflow-hidden">
                    <Button variant="destructive" className="flex-1 min-w-0"
                    onClick={() => {
                        if(voting?.target_type === VotingType.INFORMAL)
                            sendMessage({type: ChairEvents.CLOSE_INFORMAL_VOTING_EVENT, payload:{}} satisfies CloseInformalVotingEvent)
                        else if(voting?.target_type === VotingType.PROCEDURAL)
                            sendMessage({type: ChairEvents.CLOSE_PROCEDURAL_VOTING_EVENT, payload: {}} satisfies CloseProceduralVotingEvent)
                    }}>
                        Encerrar votação
                    </Button>

                </div>
            )}
            <Separator></Separator>

        </div>)
}
