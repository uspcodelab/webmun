import { useCommitteeStore } from "@/store/useCommitteeStore"
import { RollCallChoice, SessionRoles } from "@/schemas/types.gen"
import { Button } from "@/components/ui/button"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { useSession } from "@/context/SessionContext"

export default function RollCall() {
    const presentDelegations = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice !== RollCallChoice.ABSENT).length)
    const absentDelegations = useCommitteeStore((state) => Object.entries(state.roll_call?.registry ?? {}).filter(([, choice]) => choice === RollCallChoice.ABSENT).length)
    const totalDelegations = useCommitteeStore((state) => Object.keys(state.delegations).length)

    const { role } = useSession()
    const isChair = role === SessionRoles.CHAIR

    return (
        <div>
            <div className="mr-4 mb-2 ml-4 mt-4 ">
                <h2 className="text-xl font-bold">Quorum</h2>
                <p className="ml-auto text-muted-foreground">Responda o quorum</p>
            </div>

            <div className="m-4 flex flex-col gap-2">
                <div
                    className="relative h-8 w-full overflow-hidden rounded-full border bg-gray-100"
                    role="img"
                    aria-label={`Resultados: ${presentDelegations} presentes, ${absentDelegations} ausentes e ${totalDelegations} delegacoes`}
                >
                    <div className="absolute inset-0 flex">
                        <div
                            className="h-full bg-green-700"
                            style={{ width: `${(presentDelegations / totalDelegations) * 100 || 0}%` }}
                        />
                        <div
                            className="h-full bg-red-700"
                            style={{ width: `${(absentDelegations / totalDelegations) * 100 || 0}%` }}
                        />
                        <div
                            className="h-full bg-gray-100"
                            style={{
                                width: `${((totalDelegations - presentDelegations - absentDelegations) / totalDelegations) * 100 || 0}%`,
                                backgroundImage: "repeating-linear-gradient(135deg, transparent, transparent 6px, rgba(107, 114, 128, 0.22) 6px, rgba(107, 114, 128, 0.22) 10px)"
                            }}
                        />
                    </div>

                </div>
                <div className="flex flex-row gap-2 justify-center my-4">
                    <p>{presentDelegations} presentes e {absentDelegations} ausentes de {totalDelegations} delegacoes</p>
                </div>
                {!isChair &&
                    <div className="flex flex-row mt-4" >
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button className="flex-1 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap bg-green-800 text-white hover:bg-green-700">
                                    Presente e votante
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Você é considerado presente, e NÃO pode abster em votações substanciais.</p>
                            </TooltipContent>
                        </Tooltip>
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <Button className="flex-1 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap bg-green-800 text-white hover:bg-green-700">
                                    Presente
                                </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Você é considerado presente, e pode abster em votações substanciais.</p>
                            </TooltipContent>
                        </Tooltip>
                    </div>
                }
            </div>

        </div>
    )
}