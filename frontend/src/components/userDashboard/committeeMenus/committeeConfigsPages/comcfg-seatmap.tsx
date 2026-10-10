import * as React from "react"
import { CircleFlag } from "react-circle-flags"

import { Button } from "@/components/ui/button"
import {
    Combobox,
    ComboboxContent,
    ComboboxEmpty,
    ComboboxInput,
    ComboboxItem,
    ComboboxList,
} from "@/components/ui/combobox"
import { Field, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { cn } from "@/lib/utils"


// Placeholder data until this is wired to the committee's representations.
const delegationCodes: Record<string, string> = {
    Alemanha: "de",
    Brasil: "br",
    China: "cn",
    "Estados Unidos": "us",
    França: "fr",
    Índia: "in",
    Japão: "jp",
    Nigéria: "ng",
    "Reino Unido": "gb",
    Rússia: "ru",
    "África do Sul": "za",
    Argentina: "ar",
}
const delegations = Object.keys(delegationCodes)

// The session map fills a 75vw x 82vh area (the rest of the page is the 25% sidebar).
// On a 16:9 screen that is ~1.626:1. The frame below keeps that ratio and sizes seats in
// container units (6vh of 82vh = 7.3% of the frame height), so both screens lay out the same.
const SESSION_MAP_ASPECT = 1.626
const SESSION_SEAT_SIZE = "size-[7.3cqh]"

// The group is h-8 like an Input: 4px padding + h-6 items.
const TOGGLE_GROUP_CLASS = "h-8 rounded-md bg-gray-100 p-1"
const TOGGLE_ITEM_CLASS =
    "h-6 min-w-6 text-muted-foreground hover:text-black data-[state=on]:bg-white data-[state=on]:text-black"

type MapKind = "premade" | "custom"
type Shape = "semicircle" | "grid"

const MAX_SEMICIRCLES = 4
const MAX_SEATS_PER_SEMICIRCLE = 40
const MAX_GRID_SIZE = 20

function clampInt(value: string, min: number, max: number) {
    const parsed = Number.parseInt(value, 10)
    if (Number.isNaN(parsed)) return min
    return Math.min(max, Math.max(min, parsed))
}

type SemicircleSeat = { key: string; left: number; top: number }

// Same geometry as the session delegation map.
function buildSemicircleSeats(seatsPerSemicircle: number[]) {
    const seats: SemicircleSeat[] = []
    const radiusStep = 50
    const baseRadius = 120
    const centerX = 50
    const centerY = 92
    const angleRange = 160
    const startAngle = 190

    seatsPerSemicircle.forEach((seatCount, circleIndex) => {
        const radius = baseRadius + circleIndex * radiusStep
        const step = seatCount === 1 ? 0 : angleRange / (seatCount - 1)

        for (let seatIndex = 0; seatIndex < seatCount; seatIndex++) {
            const angleRad = ((startAngle + seatIndex * step) * Math.PI) / 180
            seats.push({
                key: `${circleIndex + 1}-${seatIndex + 1}`,
                left: centerX + (radius * Math.cos(angleRad)) / 6,
                top: centerY + (radius * Math.sin(angleRad)) / 3.14,
            })
        }
    })
    return seats
}

// Row 1 is the one closest to the chair (bottom), so rows are listed top to bottom in
// descending order; columns run left to right.
function buildGridSeatKeys(rows: number, columns: number) {
    const keys: string[] = []
    for (let row = rows; row >= 1; row--) {
        for (let column = 1; column <= columns; column++) {
            keys.push(`${row}-${column}`)
        }
    }
    return keys
}

type SeatButtonProps = {
    seatKey: string
    delegation?: string
    active: boolean
    sizeClassName: string
    onSelect: (seatKey: string, element: HTMLElement) => void
}

function SeatButton({ seatKey, delegation, active, sizeClassName, onSelect }: SeatButtonProps) {
    const code = delegation ? delegationCodes[delegation] : undefined

    return (
        <div className="flex flex-col items-center gap-1">
            <div className="relative">
                <Button
                    type="button"
                    variant="outline"
                    aria-label={`Assento ${seatKey}${delegation ? `, ${delegation}` : ""}`}
                    onClick={(event) => onSelect(seatKey, event.currentTarget)}
                    className={cn(
                        "overflow-hidden rounded-full p-0 text-[11px] font-medium ring-4 ring-offset-white",
                        sizeClassName,
                        delegation
                            ? "ring-sky-300/50 hover:bg-sky-100"
                            : "bg-white text-neutral-600 ring-neutral-300/30",
                        active && "ring-sky-500/60"
                    )}
                >
                    {code ? (
                        <span className="flex h-full w-full items-center justify-center overflow-hidden rounded-full">
                            <CircleFlag countryCode={code} className="scale-110 object-contain" />
                        </span>
                    ) : (
                        seatKey
                    )}
                </Button>
                {code && (
                    <span className="pointer-events-none absolute -top-1 -left-1 rounded-full border border-neutral-300 bg-white px-1 text-[9px] leading-4 font-medium text-neutral-700">
                        {seatKey}
                    </span>
                )}
            </div>
            <span className="max-w-20 truncate text-[10px] leading-none font-medium text-neutral-600">
                {delegation ?? " "}
            </span>
        </div>
    )
}

export default function CommitteeSeatmap() {
    const [mapKind, setMapKind] = React.useState<MapKind>("premade")
    const [shape, setShape] = React.useState<Shape>("semicircle")
    const [semicirclesInput, setSemicirclesInput] = React.useState("3")
    // Seats per semicircle. Kept even for semicircles that are currently hidden, so
    // lowering and raising the count again doesn't lose the numbers.
    const [seatCountInputs, setSeatCountInputs] = React.useState<string[]>(["12", "12", "12"])
    const [rowsInput, setRowsInput] = React.useState("4")
    const [columnsInput, setColumnsInput] = React.useState("6")

    // seat key -> delegation name
    const [assignments, setAssignments] = React.useState<Record<string, string>>({})
    const [activeSeat, setActiveSeat] = React.useState<string | null>(null)
    const [anchor, setAnchor] = React.useState<HTMLElement | null>(null)
    const [pickerOpen, setPickerOpen] = React.useState(false)

    const semicircles = clampInt(semicirclesInput, 1, MAX_SEMICIRCLES)
    const seatsPerSemicircle = Array.from({ length: semicircles }, (_, index) =>
        clampInt(
            seatCountInputs[index] ?? seatCountInputs[seatCountInputs.length - 1] ?? "12",
            1,
            MAX_SEATS_PER_SEMICIRCLE
        )
    )
    const rows = clampInt(rowsInput, 1, MAX_GRID_SIZE)
    const columns = clampInt(columnsInput, 1, MAX_GRID_SIZE)

    const seatsKey = seatsPerSemicircle.join(",")
    const semicircleSeats = React.useMemo(
        () => buildSemicircleSeats(seatsKey.split(",").map(Number)),
        [seatsKey]
    )
    const gridSeatKeys = React.useMemo(() => buildGridSeatKeys(rows, columns), [rows, columns])

    // Assignments only count for seats that exist in the current layout.
    const visibleAssignments = React.useMemo(() => {
        const keys = new Set(
            shape === "semicircle" ? semicircleSeats.map((seat) => seat.key) : gridSeatKeys
        )
        return Object.fromEntries(Object.entries(assignments).filter(([key]) => keys.has(key)))
    }, [assignments, shape, semicircleSeats, gridSeatKeys])

    const assignedDelegations = new Set(Object.values(visibleAssignments))
    const activeDelegation = activeSeat ? visibleAssignments[activeSeat] : undefined

    function setSeatCount(index: number, value: string) {
        setSeatCountInputs((current) => {
            const next = Array.from(
                { length: Math.max(current.length, semicircles) },
                (_, i) => current[i] ?? String(seatsPerSemicircle[i] ?? 12)
            )
            next[index] = value
            return next
        })
    }

    function selectSeat(seatKey: string, element: HTMLElement) {
        setActiveSeat(seatKey)
        setAnchor(element)
        setPickerOpen(true)
    }

    function assignDelegation(delegation: string | null) {
        if (!activeSeat || !delegation) return
        setAssignments((current) => ({ ...current, [activeSeat]: delegation }))
        setPickerOpen(false)
    }

    function clearSeat() {
        if (!activeSeat) return
        setAssignments((current) => {
            const next = { ...current }
            delete next[activeSeat]
            return next
        })
        setPickerOpen(false)
    }

    function saveAllocations() {
        // TODO: persist `visibleAssignments` once this is wired to the backend.
    }

    function clearAllSeats() {
        setAssignments({})
        setPickerOpen(false)
    }

    return (
        <div className="flex w-full flex-col gap-4">
            <div className="flex flex-wrap items-end justify-center gap-4">
                <Field className="w-fit">
                    <FieldLabel id="seatmap-kind-label" className="w-full justify-center text-center">
                        Tipo de mapa
                    </FieldLabel>
                    <ToggleGroup
                        type="single"
                        aria-labelledby="seatmap-kind-label"
                        value={mapKind}
                        onValueChange={(value) => value && setMapKind(value as MapKind)}
                        className={TOGGLE_GROUP_CLASS}
                    >
                        <ToggleGroupItem value="premade" className={TOGGLE_ITEM_CLASS}>
                            Pré-definido
                        </ToggleGroupItem>
                        <ToggleGroupItem value="custom" className={TOGGLE_ITEM_CLASS}>
                            Personalizado
                        </ToggleGroupItem>
                    </ToggleGroup>
                </Field>

                {mapKind === "premade" && (
                    <>
                        <Field className="w-fit">
                            <FieldLabel id="seatmap-shape-label" className="w-full justify-center text-center">
                                Formato
                            </FieldLabel>
                            <ToggleGroup
                                type="single"
                                aria-labelledby="seatmap-shape-label"
                                value={shape}
                                onValueChange={(value) => value && setShape(value as Shape)}
                                className={TOGGLE_GROUP_CLASS}
                            >
                                <ToggleGroupItem value="semicircle" className={TOGGLE_ITEM_CLASS}>
                                    Semicírculo
                                </ToggleGroupItem>
                                <ToggleGroupItem value="grid" className={TOGGLE_ITEM_CLASS}>
                                    Grade
                                </ToggleGroupItem>
                            </ToggleGroup>
                        </Field>

                        {shape === "semicircle" ? (
                            <>
                                <Field className="w-40">
                                    <FieldLabel htmlFor="seatmap-semicircles" className="w-full justify-center text-center">
                                        Semicírculos
                                    </FieldLabel>
                                    <Input
                                        id="seatmap-semicircles"
                                        type="number"
                                        min={1}
                                        max={MAX_SEMICIRCLES}
                                        value={semicirclesInput}
                                        onChange={(event) => setSemicirclesInput(event.target.value)}
                                    />
                                </Field>
                                {seatsPerSemicircle.map((seatCount, index) => (
                                    <Field key={index} className="w-40">
                                        <FieldLabel htmlFor={`seatmap-seats-${index}`} className="w-full justify-center text-center">
                                            Assentos do {index + 1}º semicírculo
                                        </FieldLabel>
                                        <Input
                                            id={`seatmap-seats-${index}`}
                                            type="number"
                                            min={1}
                                            max={MAX_SEATS_PER_SEMICIRCLE}
                                            value={seatCountInputs[index] ?? String(seatCount)}
                                            onChange={(event) => setSeatCount(index, event.target.value)}
                                        />
                                    </Field>
                                ))}
                            </>
                        ) : (
                            <>
                                <Field className="w-32">
                                    <FieldLabel htmlFor="seatmap-rows" className="w-full justify-center text-center">Linhas</FieldLabel>
                                    <Input
                                        id="seatmap-rows"
                                        type="number"
                                        min={1}
                                        max={MAX_GRID_SIZE}
                                        value={rowsInput}
                                        onChange={(event) => setRowsInput(event.target.value)}
                                    />
                                </Field>
                                <Field className="w-32">
                                    <FieldLabel htmlFor="seatmap-columns" className="w-full justify-center text-center">Colunas</FieldLabel>
                                    <Input
                                        id="seatmap-columns"
                                        type="number"
                                        min={1}
                                        max={MAX_GRID_SIZE}
                                        value={columnsInput}
                                        onChange={(event) => setColumnsInput(event.target.value)}
                                    />
                                </Field>
                            </>
                        )}
                    </>
                )}
            </div>

            {mapKind === "premade" && shape === "semicircle" && (
                <div
                    className="relative w-full max-w-5xl self-center overflow-hidden rounded-2xl border border-neutral-300 bg-linear-to-b from-white to-neutral-50 @container-[size]"
                    style={{ aspectRatio: SESSION_MAP_ASPECT }}
                >
                    <div className="pointer-events-none absolute top-[90%] left-1/2 flex h-[7.3cqh] w-[25.6cqh] -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-lg border border-neutral-300 bg-neutral-50 text-[11px] font-medium text-neutral-600 shadow-sm">
                        MESA
                    </div>

                    {semicircleSeats.map((seat) => (
                        <div
                            key={seat.key}
                            className="absolute"
                            style={{
                                left: `${seat.left}%`,
                                top: `${seat.top}%`,
                                transform: "translate(-50%, -50%)",
                            }}
                        >
                            <SeatButton
                                seatKey={seat.key}
                                delegation={visibleAssignments[seat.key]}
                                active={pickerOpen && activeSeat === seat.key}
                                sizeClassName={SESSION_SEAT_SIZE}
                                onSelect={selectSeat}
                            />
                        </div>
                    ))}
                </div>
            )}

            {mapKind === "premade" && shape === "grid" && (
                <div className="w-full overflow-auto rounded-2xl border border-neutral-300 bg-linear-to-b from-white to-neutral-50 p-6">
                    <div
                        className="mx-auto grid w-fit gap-x-4 gap-y-3"
                        style={{ gridTemplateColumns: `repeat(${columns}, minmax(0, auto))` }}
                    >
                        {gridSeatKeys.map((seatKey) => (
                            <SeatButton
                                key={seatKey}
                                seatKey={seatKey}
                                delegation={visibleAssignments[seatKey]}
                                active={pickerOpen && activeSeat === seatKey}
                                sizeClassName="size-11"
                                onSelect={selectSeat}
                            />
                        ))}
                        <div className="col-span-full mt-3 flex h-10 w-44 items-center justify-center justify-self-center rounded-lg border border-neutral-300 bg-neutral-50 text-[11px] font-medium text-neutral-600 shadow-sm">
                            MESA
                        </div>
                    </div>
                </div>
            )}

            {mapKind === "premade" && (
                <div className="flex flex-wrap items-center justify-center gap-2">
                    <Button
                        type="button"
                        variant="destructive"
                        disabled={Object.keys(visibleAssignments).length === 0}
                        onClick={clearAllSeats}
                    >
                        Limpar alocações
                    </Button>
                    <Button type="button" onClick={saveAllocations}>
                        Salvar alocações
                    </Button>
                </div>
            )}

            <Combobox
                items={delegations}
                value={activeDelegation ?? null}
                onValueChange={assignDelegation}
                open={pickerOpen}
                onOpenChange={setPickerOpen}
            >
                <ComboboxContent anchor={anchor} className="w-64 p-1">
                    <ComboboxInput
                        placeholder={`Delegação do assento ${activeSeat ?? ""}`}
                        showTrigger={false}
                    />
                    <ComboboxEmpty>Nenhuma delegação encontrada.</ComboboxEmpty>
                    <ComboboxList>
                        {(delegation: string) => (
                            <ComboboxItem
                                key={delegation}
                                value={delegation}
                                disabled={assignedDelegations.has(delegation) && delegation !== activeDelegation}
                            >
                                <CircleFlag
                                    countryCode={delegationCodes[delegation]}
                                    height={16}
                                    width={16}
                                    className="size-4 shrink-0"
                                />
                                {delegation}
                                
                            </ComboboxItem>
                        )}
                    </ComboboxList>
                    {activeDelegation && (
                        <Button variant="destructive" size="sm" className="m-1 w-[calc(100%-0.5rem)]" onClick={clearSeat}>
                            Remover alocação
                        </Button>
                    )}
                </ComboboxContent>
            </Combobox>
        </div>
    )
}
