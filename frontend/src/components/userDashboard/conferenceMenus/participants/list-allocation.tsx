import * as React from "react"
import {
	type ColumnDef,
	type ColumnFiltersState,
	type SortingState,
	type VisibilityState,
	flexRender,
	getCoreRowModel,
	getFilteredRowModel,
	getPaginationRowModel,
	getSortedRowModel,
	useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select"
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table"

type Participant = {
	id: string
	name: string
	email: string
	committee: string
	representation: string
}

const committeeOptions = [
	"Security Council",
	"UNICEF",
	"UNHRC",
	"WHO",
	"ECOSOC",
]

const representationOptions = [
	"Brazil",
	"United States",
	"France",
	"Japan",
	"Nigeria",
	"Mexico",
]

const initialParticipants: Participant[] = [
	{
		id: "33f0e8f6-0cc7-4cc8-a6ff-f4f6bca6a467",
		name: "Ana Martins",
		email: "ana.martins@example.com",
		committee: "Security Council",
		representation: "Brazil",
	},
	{
		id: "88c48914-d4e2-48bf-b4f2-8d0f23f035e9",
		name: "Diego Costa",
		email: "diego.costa@example.com",
		committee: "UNICEF",
		representation: "Mexico",
	},
	{
		id: "8f66643e-11c9-4ee0-adbe-906cefd86f45",
		name: "Sara Thompson",
		email: "sara.thompson@example.com",
		committee: "WHO",
		representation: "United States",
	},
	{
		id: "fd177bd7-1cbc-454b-b7a6-041566a73ed3",
		name: "Kenji Sato",
		email: "kenji.sato@example.com",
		committee: "UNHRC",
		representation: "Japan",
	},
	{
		id: "131902c1-9c6f-4657-b46f-a6f8247693c4",
		name: "Claire Dubois",
		email: "claire.dubois@example.com",
		committee: "ECOSOC",
		representation: "France",
	},
]

export default function ParticipantListAllocation() {
	const [participants, setParticipants] = React.useState<Participant[]>(initialParticipants)
	const [sorting, setSorting] = React.useState<SortingState>([])
	const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
	const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
	const [rowSelection, setRowSelection] = React.useState({})

	const updateParticipant = React.useCallback(
		(id: string, field: "committee" | "representation", value: string) => {
			setParticipants((currentParticipants) =>
				currentParticipants.map((participant) =>
					participant.id === id ? { ...participant, [field]: value } : participant
				)
			)
		},
		[]
	)

	const columns = React.useMemo<ColumnDef<Participant>[]>(
		() => [
			{
				id: "select",
				header: ({ table }) => (
					<Checkbox
						checked={
							table.getIsAllPageRowsSelected() ||
							(table.getIsSomePageRowsSelected() && "indeterminate")
						}
						onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
						aria-label="Selecionar todos"
					/>
				),
				cell: ({ row }) => (
					<Checkbox
						checked={row.getIsSelected()}
						onCheckedChange={(value) => row.toggleSelected(!!value)}
						aria-label="Selecionar participante"
					/>
				),
				enableSorting: false,
				enableHiding: false,
			},
			{
				accessorKey: "name",
				header: ({ column }) => (
					<Button
						variant="ghost"
						onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
					>
						Nome
						<ArrowUpDown className="ml-2" />
					</Button>
				),
			},
			{
				accessorKey: "email",
				header: ({ column }) => (
					<Button
						variant="ghost"
						onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
					>
						Email
						<ArrowUpDown className="ml-2" />
					</Button>
				),
			},
			{
				accessorKey: "committee",
				header: ({ column }) => (
					<Button
						variant="ghost"
						onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
					>
						Comitê
						<ArrowUpDown className="ml-2" />
					</Button>
				),
				cell: ({ row }) => (
					<Select
						value={row.original.committee}
						onValueChange={(value) => updateParticipant(row.original.id, "committee", value)}
					>
						<SelectTrigger className="w-55">
							<SelectValue placeholder="Selecionar comitê" />
						</SelectTrigger>
						<SelectContent align="start">
							{committeeOptions.map((committee) => (
								<SelectItem key={committee} value={committee}>
									{committee}
								</SelectItem>
							))}
						</SelectContent>
					</Select>
				),
			},
			{
				accessorKey: "representation",
				header: ({ column }) => (
					<Button
						variant="ghost"
						onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
					>
						Representação
						<ArrowUpDown className="ml-2" />
					</Button>
				),
				cell: ({ row }) => (
					<Select
						value={row.original.representation}
						onValueChange={(value) =>
							updateParticipant(row.original.id, "representation", value)
						}
					>
						<SelectTrigger className="w-55">
							<SelectValue placeholder="Selecionar representação" />
						</SelectTrigger>
						<SelectContent align="start">
							{representationOptions.map((representation) => (
								<SelectItem key={representation} value={representation}>
									{representation}
								</SelectItem>
							))}
						</SelectContent>
					</Select>
				),
			},
		],
		[updateParticipant]
	)

	const table = useReactTable({
		data: participants,
		columns,
		onSortingChange: setSorting,
		onColumnFiltersChange: setColumnFilters,
		onColumnVisibilityChange: setColumnVisibility,
		onRowSelectionChange: setRowSelection,
		getCoreRowModel: getCoreRowModel(),
		getPaginationRowModel: getPaginationRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFilteredRowModel: getFilteredRowModel(),
		state: {
			sorting,
			columnFilters,
			columnVisibility,
			rowSelection,
		},
	})

	function deleteSelectedParticipants() {
		const selectedIds = new Set(
			table.getFilteredSelectedRowModel().rows.map((row) => row.original.id)
		)

		if (selectedIds.size === 0) {
			return
		}

		setParticipants((currentParticipants) =>
			currentParticipants.filter((participant) => !selectedIds.has(participant.id))
		)
		setRowSelection({})
	}

	const selectedCount = table.getFilteredSelectedRowModel().rows.length

	return (
		<div className="flex flex-col gap-4">
			<div>
				<h1 className="text-2xl font-bold">Listagem e alocação de participantes</h1>
				<p className="text-muted-foreground">
					Visualize participantes, pesquise por nome e ajuste comitê e representação.
				</p>
			</div>

			<div className="rounded-3xl border border-border bg-background p-4 shadow-sm">
				<div className="flex flex-col gap-3 pb-4 md:flex-row md:items-center">
					<Input
						placeholder="Pesquisar por nome..."
						value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
						onChange={(event) =>
							table.getColumn("name")?.setFilterValue(event.target.value)
						}
						className="w-full md:max-w-sm"
					/>

					<div className="flex flex-wrap items-center gap-2 md:ml-auto">
						<DropdownMenu>
							<DropdownMenuTrigger asChild>
								<Button variant="outline">
									Colunas
									<ChevronDown className="ml-2" />
								</Button>
							</DropdownMenuTrigger>
							<DropdownMenuContent align="end">
								{table
									.getAllColumns()
									.filter((column) => column.getCanHide())
									.map((column) => (
										<DropdownMenuCheckboxItem
											key={column.id}
											className="capitalize"
											checked={column.getIsVisible()}
											onCheckedChange={(value) => column.toggleVisibility(!!value)}
										>
											{column.id}
										</DropdownMenuCheckboxItem>
									))}
							</DropdownMenuContent>
						</DropdownMenu>

						<Button
							variant="destructive"
							onClick={deleteSelectedParticipants}
							disabled={selectedCount === 0}
						>
							Excluir selecionados
						</Button>
					</div>
				</div>

				<div className="overflow-hidden rounded-xl border">
					<Table>
						<TableHeader>
							{table.getHeaderGroups().map((headerGroup) => (
								<TableRow key={headerGroup.id}>
									{headerGroup.headers.map((header) => (
										<TableHead key={header.id}>
											{header.isPlaceholder
												? null
												: flexRender(
														header.column.columnDef.header,
														header.getContext()
													)}
										</TableHead>
									))}
								</TableRow>
							))}
						</TableHeader>
						<TableBody>
							{table.getRowModel().rows.length > 0 ? (
								table.getRowModel().rows.map((row) => (
									<TableRow
										key={row.id}
										data-state={row.getIsSelected() ? "selected" : undefined}
									>
										{row.getVisibleCells().map((cell) => (
											<TableCell key={cell.id}>
												{flexRender(cell.column.columnDef.cell, cell.getContext())}
											</TableCell>
										))}
									</TableRow>
								))
							) : (
								<TableRow>
									<TableCell colSpan={columns.length} className="h-24 text-center">
										Nenhum participante encontrado.
									</TableCell>
								</TableRow>
							)}
						</TableBody>
					</Table>
				</div>

				<div className="flex flex-col gap-2 pt-4 md:flex-row md:items-center md:justify-between">
					<p className="text-sm text-muted-foreground">
						{selectedCount} de {table.getFilteredRowModel().rows.length} participante(s) selecionado(s).
					</p>

					<div className="flex items-center gap-2">
						<Button
							variant="outline"
							size="sm"
							onClick={() => table.previousPage()}
							disabled={!table.getCanPreviousPage()}
						>
							Anterior
						</Button>
						<Button
							variant="outline"
							size="sm"
							onClick={() => table.nextPage()}
							disabled={!table.getCanNextPage()}
						>
							Próxima
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
