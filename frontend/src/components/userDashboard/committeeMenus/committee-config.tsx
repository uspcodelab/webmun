import { useState } from "react"
import { useParams } from "react-router-dom"

import {
    ToggleGroup,
    ToggleGroupItem,
} from "@/components/ui/toggle-group"

import { useConference } from "@/context/ConferenceContext"

import CommitteeRepresentations from "./committeeConfigsPages/comcfg-representations"
import CommitteeSeatmap from "./committeeConfigsPages/comcfg-seatmap"

export default function CommitteeConfig() {
    const { committeeId } = useParams()
    const { committees } = useConference()
    const committee = committees.find((item) => item.id === Number(committeeId))
    const [filter, setFilter] = useState("representations")

    if (!committee) return <p className="text-muted-foreground">Comitê não encontrado.</p>

    return (
        <div className="flex flex-col items-center justify-center gap-4">
            <h1 className="text-2xl font-bold">Configure o(a) {committee.name}</h1>
            <ToggleGroup
                type="single"
                value={filter}
                onValueChange={(value) => value && setFilter(value)}
                className="bg-gray-100 rounded-md p-1"
            >
                <ToggleGroupItem value="representations" aria-label="Toggle all" className="text-muted-foreground hover:text-black data-[state=on]:bg-white data-[state=on]:text-black">
                    Representações
                </ToggleGroupItem>
                <ToggleGroupItem value="seatmap" aria-label="Toggle seatmap" className="text-muted-foreground hover:text-black data-[state=on]:bg-white data-[state=on]:text-black">
                    Mapa de Assentos
                </ToggleGroupItem>
                <ToggleGroupItem value="rules" aria-label="Toggle rules" className="text-muted-foreground hover:text-black data-[state=on]:bg-white data-[state=on]:text-black">
                    Regras do Comitê
                </ToggleGroupItem>
            </ToggleGroup>
            {filter === "representations" && (
                <CommitteeRepresentations />
            )}
            {filter === "seatmap" && (
                <CommitteeSeatmap />
            )}
        </div>
    )
}
