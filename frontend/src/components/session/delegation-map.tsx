import { Button } from "@/components/ui/button"

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
                    className="pointer-events-none absolute left-1/2 top-[90%] h-10 w-28 -translate-x-1/2 -translate-y-1/2 rounded-lg border border-neutral-300 bg-white shadow-sm"
                >
                    <div className="flex h-full w-full items-center justify-center rounded-lg bg-neutral-50 text-[11px] font-medium text-neutral-600">
                        MESA
                    </div>
                </div>

                {circles.map((circleIndex) => {
                    const radiusStep = 40
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
                                        <Button
                                            type="button"
                                            variant="outline"
                                            className="h-12 w-12 rounded-full p-0 text-[10px]"
                                        >
                                            {circleIndex + 1}-{seatIndex + 1}
                                        </Button>
                                        <span className="text-[10px] font-medium leading-none text-neutral-600">
                                            {circleIndex + 1}-{seatIndex + 1}
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
