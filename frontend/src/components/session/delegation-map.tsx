import { Button } from "@/components/ui/button"
// Dropdown menu removed in favor of context menu

import {
    ContextMenu,
    ContextMenuContent,
    ContextMenuGroup,
    ContextMenuItem,
    ContextMenuLabel,
    ContextMenuSeparator,
    ContextMenuSub,
    ContextMenuSubContent,
    ContextMenuSubTrigger,
    ContextMenuTrigger,
} from "@/components/ui/context-menu"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { CircleFlag } from 'react-circle-flags'
import { sendMessage } from "@/context/SessionContext"
import { type AddGslSpeakerEvent, type MarkRollCallEvent, type GrantFloorEvent, ChairEvents, RollCallChoice, type CedeTimeEvent } from "@/schemas/types.gen"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { useSession } from "@/context/SessionContext"

import { States, VotingChoice, SessionRoles } from '@/schemas/types.gen';
import { useEffect, useState } from "react"


type DelegationMapProps = {
    semicircleCount?: number
    buttonsPerSemicircle?: number | number[]
    presentDelegations?: number
}

export default function DelegationMap({
    semicircleCount = 3,
    buttonsPerSemicircle = 12,
}: DelegationMapProps) {

    const { role } = useSession()
    const isChair = role === SessionRoles.CHAIR

    const circles = Array.from({ length: Math.max(1, semicircleCount) }, (_, i) => i)

    const getSeatCount = (circleIndex: number) => {
        if (Array.isArray(buttonsPerSemicircle)) {
            const fallback = buttonsPerSemicircle[buttonsPerSemicircle.length - 1] ?? 1
            return Math.max(1, buttonsPerSemicircle[circleIndex] ?? fallback)
        }

        return Math.max(1, buttonsPerSemicircle)
    }

    const delegationsById = useCommitteeStore((state) => state.delegations)
    const delegationsBySeat = new Map(
        Object.values(delegationsById).map((delegation) => [
            delegation.seat,
            delegation,
        ])
    )

    const rcregistry = useCommitteeStore((state) => state.roll_call.registry)
    const presentDelegations = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice !== RollCallChoice.ABSENT).length)
    const totalDelegations = useCommitteeStore((state) => Object.keys(state.delegations).length)
    const simpleMajority = Math.floor(presentDelegations / 2) + 1
    const qualifiedMajority = Math.ceil((presentDelegations * 2) / 3)
    const currentState = useCommitteeStore((state) => state.current_state)

    const votingRegistry = useCommitteeStore((state) => state.voting?.voting_registry ?? null)



    const getDelegationRingColor = (state: string | undefined, presence: string | undefined, vote: VotingChoice | null) => {
        switch (state) {
            case States.ROLL_CALL:
                if (presence === RollCallChoice.PRESENT_AND_VOTING) return "ring-green-700/50"
                if (presence === RollCallChoice.PRESENT) return "ring-green-500/50"
                if (presence === RollCallChoice.ABSENT) return "ring-red-500/50"
                return "ring-sky-300/30"
            case States.VOTING_EXECUTION:
                if (vote === VotingChoice.FAVOUR) return "ring-green-500/50"
                if (vote === VotingChoice.YES_WITH_RIGHTS) return "ring-green-300/50"
                if (vote === VotingChoice.AGAINST) return "ring-red-500/50"
                if (vote === VotingChoice.NO_WITH_RIGHTS) return "ring-red-300/50"
                if (vote === VotingChoice.ABSTAIN) return "ring-gray-400/50"
                return "ring-neutral-300/30"
            default:
                if (presence == RollCallChoice.PRESENT_AND_VOTING || presence === RollCallChoice.PRESENT) return "ring-sky-300/50"
                return "ring-neutral-400/30"
        }
    }

    const [active, setActive] = useState(false)

    useEffect(()=>{
    
        const setAc = (e : CustomEvent) => {if (e.detail.type === "cedetime") setActive(true)};

        window.addEventListener("mapselection", setAc as EventListener);

        return () => { window.removeEventListener("mapselection", setAc as EventListener)}
    }, []);

    return (
        <div className="relative h-full w-full overflow-hidden">
            <div className="absolute inset-0 m-3 rounded-2xl border border-neutral-300 bg-linear-to-b from-white to-neutral-50">
                <div className="pointer-events-none absolute left-4 top-4 rounded-md border border-neutral-200 bg-white/90 px-3 py-2 text-xs text-neutral-600 shadow-sm">
                    <div className="font-medium text-neutral-800">Delegações presentes:</div>
                    <div>{presentDelegations}/{totalDelegations} delegações</div>
                </div>

                <div className="pointer-events-none absolute left-1/2 top-4 -translate-x-1/2 rounded-md border border-neutral-200 bg-white/90 px-3 py-2 text-center text-xs text-neutral-600 shadow-sm">
                    <div className="font-medium text-neutral-800">Status da sessão</div>
                    <div>{currentState}</div>
                </div>

                <div className="pointer-events-none absolute right-4 top-4 rounded-md border border-neutral-200 bg-white/90 px-3 py-2 text-right text-xs text-neutral-600 shadow-sm">
                    <div className="font-medium text-neutral-800">Maioria de votacao</div>
                    <div>Maioria simples: {simpleMajority} votos</div>
                    <div>Maioria qualificada: {qualifiedMajority} votos</div>
                </div>

                <div
                    className="pointer-events-none absolute left-1/2 top-[90%] h-[6vh] w-[21vh] -translate-x-1/2 -translate-y-1/2 rounded-lg border border-neutral-300 bg-white shadow-sm"
                >
                    <div className="flex h-full w-full items-center justify-center rounded-lg bg-neutral-50 text-[11px] font-medium text-neutral-600">
                        MESA
                    </div>
                </div>

                {circles.map((circleIndex) => {
                    const radiusStep = 50
                    const baseRadius = 120
                    const radius = baseRadius + circleIndex * radiusStep
                    const centerX = 50
                    const centerY = 92
                    const seatCount = getSeatCount(circleIndex)
                    const seats = Array.from({ length: seatCount }, (_, i) => i)

                    return (
                        <div key={`ring-${circleIndex}`} >


                            {seats.map((seatIndex) => {
                                const angleRange = 160
                                const startAngle = 190
                                const step = seatCount === 1 ? 0 : angleRange / (seatCount - 1)
                                const angleDeg = startAngle + seatIndex * step
                                const angleRad = (angleDeg * Math.PI) / 180
                                const x = centerX + (radius * Math.cos(angleRad)) / 6
                                const y = centerY + (radius * Math.sin(angleRad)) / 3.14
                                const seat = `${circleIndex + 1}-${seatIndex + 1}`
                                const delegation = delegationsBySeat.get(seat)

                                const presence = rcregistry && delegation ? rcregistry[delegation.id] : "None"
                                const vote = votingRegistry && delegation ? votingRegistry[delegation.id] : null
                                const ringcolor = getDelegationRingColor(currentState, presence, vote)

                                if (!delegation) {
                                    return <div key={`empty-seat-${seat}`} />
                                }
                                return (
                                    <div
                                        key={`ring-${circleIndex}-seat-${seatIndex}`}
                                        className="absolute flex flex-col items-center gap-1"
                                        style={{
                                            left: `${x}%`,
                                            top: `${y}%`,
                                            transform: "translate(-50%, -50%)",
                                        }}
                                    >
                                        {isChair && (
                                            <ContextMenu>
                                                <Tooltip>
                                                    <TooltipTrigger asChild>
                                                        <ContextMenuTrigger asChild>
                                                            <Button
                                                                type="button"
                                                                variant="outline"
                                                                className={`h-[6vh] w-[6vh] overflow-hidden rounded-full p-0 text-[10px] ring-4 ${ringcolor} ring-offset-white shadow-[0_0_18px_rgba(56,189,248,0.18)]`}
                                                                onClick={()=>{
                                                                    if(active)
                                                                    {
                                                                        sendMessage({type:ChairEvents.CEDE_TIME_EVENT, payload:{representation_id: delegation.id}} satisfies CedeTimeEvent)
                                                                        setActive(false);
                                                                    }
                                                                    }}
                                                            >
                                                                <span className="flex h-full w-full items-center justify-center overflow-hidden rounded-full">
                                                                    <CircleFlag
                                                                        countryCode={delegation.code}
                                                                        className="scale-110 object-contain"
                                                                    />
                                                                </span>
                                                            </Button>
                                                        </ContextMenuTrigger>
                                                    </TooltipTrigger>
                                                    {/* TODO: Replace by country full name */}
                                                    <TooltipContent>
                                                        <p>{delegation.name}</p>
                                                    </TooltipContent>
                                                </Tooltip>
                                                <ContextMenuContent className="w-60">
                                                    <ContextMenuGroup>
                                                        <ContextMenuLabel>Ações sobre a Delegação</ContextMenuLabel>
                                                        <ContextMenuItem onClick={() => sendMessage({ type: ChairEvents.ADD_GSL_SPEAKER_EVENT, payload: { representation_id: delegation.id } } satisfies AddGslSpeakerEvent)}>
                                                            Colocar na Lista de Discursos
                                                        </ContextMenuItem>
                                                        <ContextMenuItem onClick={() => sendMessage({ type: ChairEvents.GRANT_FLOOR_EVENT, payload: { representation_id: delegation.id } } satisfies GrantFloorEvent)}>
                                                            Dar a palavra
                                                        </ContextMenuItem>
                                                    </ContextMenuGroup>
                                                    <ContextMenuSeparator />
                                                    <ContextMenuGroup>
                                                        <ContextMenuItem>Ausência Temporária</ContextMenuItem>
                                                        <ContextMenuSub>
                                                            <ContextMenuSubTrigger>Mudar Presença</ContextMenuSubTrigger>
                                                            <ContextMenuSubContent>
                                                                <ContextMenuItem onClick={() => sendMessage({ type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: { delegation_id: delegation.id, choice: RollCallChoice.PRESENT_AND_VOTING } } satisfies MarkRollCallEvent)}>
                                                                    Presente Votante
                                                                </ContextMenuItem>
                                                                <ContextMenuItem onClick={() => sendMessage({ type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: { delegation_id: delegation.id, choice: RollCallChoice.PRESENT } } satisfies MarkRollCallEvent)}>
                                                                    Presente
                                                                </ContextMenuItem>
                                                                <ContextMenuItem onClick={() => sendMessage({ type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: { delegation_id: delegation.id, choice: RollCallChoice.ABSENT } } satisfies MarkRollCallEvent)}>
                                                                    Ausente
                                                                </ContextMenuItem>
                                                            </ContextMenuSubContent>
                                                        </ContextMenuSub>

                                                    </ContextMenuGroup>
                                                    <ContextMenuSeparator />
                                                    <ContextMenuGroup>
                                                        <ContextMenuSub>
                                                            <ContextMenuSubTrigger>Punições</ContextMenuSubTrigger>
                                                            <ContextMenuSubContent>
                                                                <ContextMenuItem>Aviso Formal</ContextMenuItem>
                                                                <ContextMenuItem>Expulsão</ContextMenuItem>
                                                            </ContextMenuSubContent>
                                                        </ContextMenuSub>
                                                    </ContextMenuGroup>
                                                </ContextMenuContent>
                                            </ContextMenu>)}
                                        {!isChair && (
                                            <span
                                             
                                                className={`h-[6vh] w-[6vh] overflow-hidden rounded-full p-0 text-[10px] ring-4 ${ringcolor} ring-offset-white shadow-[0_0_18px_rgba(56,189,248,0.18)]`}
                                            >
                                                <span className="flex h-full w-full items-center justify-center overflow-hidden rounded-full">
                                                    <CircleFlag
                                                        countryCode={delegation.code}
                                                        className="scale-110 object-contain"
                                                    />
                                                </span>
                                            </span>

                                        )}

                                        <span className="text-[10px] font-medium leading-none text-neutral-600">
                                            {delegation.name}
                                        </span>

                                    </div>

                                )

                            })}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
