import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuPortal,
    DropdownMenuSeparator,

    DropdownMenuSub,
    DropdownMenuSubContent,
    DropdownMenuSubTrigger,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useCommitteeStore } from "@/store/useCommitteeStore"
import Flags from "@/components/ui/flags"

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
    delegations.sort((a, b) => a.seat > b.seat? 1 : -1)
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
                                delegationIndex++    
                                if (`${circleIndex + 1 }-${seatIndex + 1}` != delegations[delegationIndex]?.seat) {
                                    return (<div></div>)}
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
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button
                                                    type="button"
                                                    variant="outline"
                                                    className="h-[6vh] w-[6vh] overflow-hidden rounded-full p-0 text-[10px] ring-4 ring-sky-300/30 ring-offset-white shadow-[0_0_18px_rgba(56,189,248,0.18)]"
                                                >
                                                    <span className="flex h-full w-full items-center justify-center overflow-hidden rounded-full">
                                                        <Flags
                                                            code={delegations[delegationIndex]?.code}
                                                            className="scale-125 object-contain"
                                                        />
                                                    </span>
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent className="w-60" align="start">
                                                <DropdownMenuGroup>
                                                    <DropdownMenuLabel>Ações sobre a Delegação</DropdownMenuLabel>
                                                    <DropdownMenuItem>
                                                        Colocar na Lista de Discursos
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem>
                                                        Dar a palavra
                                                    </DropdownMenuItem>
                                                </DropdownMenuGroup>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuGroup>
                                                    <DropdownMenuItem>Ausência</DropdownMenuItem>
                                                    <DropdownMenuSub>
                                                        <DropdownMenuSubTrigger>Mudar Presença</DropdownMenuSubTrigger>
                                                        <DropdownMenuPortal>
                                                            <DropdownMenuSubContent>
                                                                <DropdownMenuItem>Presente Votante</DropdownMenuItem>
                                                                <DropdownMenuItem>Presente</DropdownMenuItem>
                                                                <DropdownMenuItem>Ausente</DropdownMenuItem>
                                                            </DropdownMenuSubContent>
                                                        </DropdownMenuPortal>
                                                    </DropdownMenuSub>

                                                </DropdownMenuGroup>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuGroup>
                                                    <DropdownMenuSub >
                                                        <DropdownMenuSubTrigger >Punições</DropdownMenuSubTrigger>
                                                        <DropdownMenuPortal>
                                                            <DropdownMenuSubContent>
                                                                <DropdownMenuItem>Aviso Formal</DropdownMenuItem>
                                                                <DropdownMenuItem>Expulsão</DropdownMenuItem>
                                                            </DropdownMenuSubContent>
                                                        </DropdownMenuPortal>
                                                    </DropdownMenuSub>
                                                   
                                                </DropdownMenuGroup>
                                            </DropdownMenuContent>
                                        </DropdownMenu>

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
