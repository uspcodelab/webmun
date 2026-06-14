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
import { sendMessage } from "@/pages/Session"
import { type ChairInsertQueueEvent, type MarkRollCallEvent, ChairEvents, RollCallChoice } from "@/schemas/types.gen"

type DelegationMapProps = {
    semicircleCount?: number
    buttonsPerSemicircle?: number | number[]
    presentDelegations?: number
}

export default function DelegationMap({
    semicircleCount = 3,
    buttonsPerSemicircle = 12,
    presentDelegations,
}: DelegationMapProps) {
    const circles = Array.from({ length: Math.max(1, semicircleCount) }, (_, i) => i)

    const getSeatCount = (circleIndex: number) => {
        if (Array.isArray(buttonsPerSemicircle)) {
            const fallback = buttonsPerSemicircle[buttonsPerSemicircle.length - 1] ?? 1
            return Math.max(1, buttonsPerSemicircle[circleIndex] ?? fallback)
        }

        return Math.max(1, buttonsPerSemicircle)
    }

    const delegations = useCommitteeStore((state) => state.delegations)
    delegations.sort((a, b) => a.seat > b.seat ? 1 : -1)
    let delegationIndex = -1

    const totalDelegations = circles.reduce((total, _, circleIndex) => total + getSeatCount(circleIndex), 0)
    const delegationsPresent = Math.max(0, Math.min(presentDelegations ?? totalDelegations, totalDelegations))
    const simpleMajority = Math.floor(delegationsPresent / 2) + 1
    const qualifiedMajority = Math.ceil((delegationsPresent * 2) / 3)

    return (
        <div className="relative h-full w-full overflow-hidden">
            <div className="absolute inset-0 m-6 rounded-2xl border border-neutral-300 bg-linear-to-b from-white to-neutral-50">
                <div className="pointer-events-none absolute left-4 top-4 rounded-md border border-neutral-200 bg-white/90 px-3 py-2 text-xs text-neutral-600 shadow-sm">
                    <div className="font-medium text-neutral-800">Delegações presentes:</div>
                    <div>{delegationsPresent}/{totalDelegations} delegações</div>
                </div>

                <div className="pointer-events-none absolute left-1/2 top-4 -translate-x-1/2 rounded-md border border-neutral-200 bg-white/90 px-3 py-2 text-center text-xs text-neutral-600 shadow-sm">
                    <div className="font-medium text-neutral-800">Status da sessão</div>
                    <div>Placeholder: aguardando atualização do comitê</div>
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
                                const currentDelegationIndex = delegationIndex + 1
                                delegationIndex = currentDelegationIndex

                                if (`${circleIndex + 1}-${seatIndex + 1}` != delegations[currentDelegationIndex]?.seat) {
                                    return (<div></div>)
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
                                        <ContextMenu>
                                            <ContextMenuTrigger asChild>
                                                <Button
                                                    type="button"
                                                    variant="outline"
                                                    className="h-[6vh] w-[6vh] overflow-hidden rounded-full p-0 text-[10px] ring-4 ring-sky-300/30 ring-offset-white shadow-[0_0_18px_rgba(56,189,248,0.18)]"
                                                >
                                                    <span className="flex h-full w-full items-center justify-center overflow-hidden rounded-full">
                                                        <CircleFlag
                                                            countryCode={delegations[delegationIndex]?.code}
                                                            className="scale-110 object-contain"
                                                        />
                                                    </span>
                                                </Button>
                                            </ContextMenuTrigger>
                                            <ContextMenuContent className="w-60">
                                                <ContextMenuGroup>
                                                    <ContextMenuLabel>Ações sobre a Delegação</ContextMenuLabel>
                                                    <ContextMenuItem onClick={() => sendMessage({type: ChairEvents.INSERT_QUEUE_EVENT, payload: {target: delegations[currentDelegationIndex]?.id}} as ChairInsertQueueEvent)}>
                                                        Colocar na Lista de Discursos
                                                    </ContextMenuItem>
                                                    <ContextMenuItem>
                                                        Dar a palavra
                                                    </ContextMenuItem>
                                                </ContextMenuGroup>
                                                <ContextMenuSeparator />
                                                <ContextMenuGroup>
                                                    <ContextMenuItem>Ausência</ContextMenuItem>
                                                    <ContextMenuSub>
                                                        <ContextMenuSubTrigger>Mudar Presença</ContextMenuSubTrigger>
                                                        <ContextMenuSubContent>
                                                            <ContextMenuItem onClick={() => sendMessage({type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: {delegation_id: delegations[currentDelegationIndex].id, choice: RollCallChoice.PRESENT_AND_VOTING}} as MarkRollCallEvent)}>
                                                                Presente Votante
                                                            </ContextMenuItem>
                                                            <ContextMenuItem onClick={() => sendMessage({type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: {delegation_id: delegations[currentDelegationIndex].id, choice: RollCallChoice.PRESENT}} as MarkRollCallEvent)}>
                                                                Presente
                                                            </ContextMenuItem>
                                                            <ContextMenuItem onClick={() => sendMessage({type: ChairEvents.MARK_ROLL_CALL_EVENT, payload: {delegation_id: delegations[currentDelegationIndex].id, choice: RollCallChoice.ABSENT}} as MarkRollCallEvent)}>
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
                                        </ContextMenu>

                                        <span className="text-[10px] font-medium leading-none text-neutral-600">
                                            {delegations[delegationIndex]?.name || "Vazio"}
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
