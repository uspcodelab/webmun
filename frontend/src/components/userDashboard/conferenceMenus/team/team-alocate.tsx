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

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

type TeamMember = {
  id: string
  name: string
  email: string
  roles: string[]
  assignments: string[]
}

const roleOptions = [
  "Secretary General",
  "Director",
  "Moderator",
  "Rapporteur",
  "Crisis Staff",
  "Press",
]

const assignmentOptions = [
  "Core Team",
  "Logistics",
  "Security Council",
  "UNICEF",
  "UNHRC",
  "WHO",
]

const initialTeamMembers: TeamMember[] = [
  {
    id: "a2787617-43d1-4d75-a78e-359b758436fa",
    name: "Luisa Almeida",
    email: "luisa.almeida@example.com",
    roles: ["Director", "Moderator"],
    assignments: ["Security Council"],
  },
  {
    id: "8521bc6a-bd1d-4eee-a802-f98f85a0cf03",
    name: "Mateus Silva",
    email: "mateus.silva@example.com",
    roles: ["Rapporteur"],
    assignments: ["UNICEF", "Logistics"],
  },
  {
    id: "f83ab80f-c4a1-430f-8ac7-c95e3f29fdb6",
    name: "Carla Ribeiro",
    email: "carla.ribeiro@example.com",
    roles: ["Secretary General"],
    assignments: ["Core Team"],
  },
  {
    id: "b90ea379-8673-4094-95a5-ae8ea88a2f9f",
    name: "Henrique Santos",
    email: "henrique.santos@example.com",
    roles: ["Crisis Staff", "Press"],
    assignments: ["WHO", "UNHRC"],
  },
]

function toSortedUniqueList(items: string[]) {
  return [...new Set(items)].sort((first, second) => first.localeCompare(second))
}

function MultiAssignCell({
  value,
  options,
  onToggle,
  buttonLabel,
}: {
  value: string[]
  options: string[]
  onToggle: (option: string, checked: boolean) => void
  buttonLabel: string
}) {
  const selected = toSortedUniqueList(value)

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="w-60 justify-between">
          <span className="truncate text-left">
            {selected.length > 0 ? `${selected.length} selecionado(s)` : buttonLabel}
          </span>
          <ChevronDown className="ml-2" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start">
        <DropdownMenuLabel>{buttonLabel}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {options.map((option) => (
          <DropdownMenuCheckboxItem
            key={option}
            checked={selected.includes(option)}
            onCheckedChange={(checked) => onToggle(option, !!checked)}
          >
            {option}
          </DropdownMenuCheckboxItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

function AssignmentBadges({ values }: { values: string[] }) {
  const sortedValues = toSortedUniqueList(values)

  if (sortedValues.length === 0) {
    return <span className="text-muted-foreground">Nenhum</span>
  }

  return (
    <div className="flex max-w-70 flex-wrap gap-1">
      {sortedValues.map((value) => (
        <Badge key={value} variant="secondary">
          {value}
        </Badge>
      ))}
    </div>
  )
}

export default function TeamAllocate() {
  const [teamMembers, setTeamMembers] = React.useState<TeamMember[]>(initialTeamMembers)
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})

  const toggleArrayValue = React.useCallback(
    (
      memberId: string,
      field: "roles" | "assignments",
      option: string,
      checked: boolean
    ) => {
      setTeamMembers((currentMembers) =>
        currentMembers.map((member) => {
          if (member.id !== memberId) {
            return member
          }

          const currentValues = member[field]
          const nextValues = checked
            ? [...currentValues, option]
            : currentValues.filter((item) => item !== option)

          return {
            ...member,
            [field]: toSortedUniqueList(nextValues),
          }
        })
      )
    },
    []
  )

  const columns = React.useMemo<ColumnDef<TeamMember>[]>(
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
            aria-label="Selecionar membro"
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
        id: "roles",
        accessorFn: (member) => member.roles.join(", "),
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Papéis
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => (
          <div className="space-y-2">
            <MultiAssignCell
              value={row.original.roles}
              options={roleOptions}
              buttonLabel="Atribuir papéis"
              onToggle={(option, checked) =>
                toggleArrayValue(row.original.id, "roles", option, checked)
              }
            />
            <AssignmentBadges values={row.original.roles} />
          </div>
        ),
      },
      {
        id: "assignments",
        accessorFn: (member) => member.assignments.join(", "),
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Equipes e Comitês
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => (
          <div className="space-y-2">
            <MultiAssignCell
              value={row.original.assignments}
              options={assignmentOptions}
              buttonLabel="Atribuir equipes/comitês"
              onToggle={(option, checked) =>
                toggleArrayValue(row.original.id, "assignments", option, checked)
              }
            />
            <AssignmentBadges values={row.original.assignments} />
          </div>
        ),
      },
    ],
    [toggleArrayValue]
  )

  const table = useReactTable({
    data: teamMembers,
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

  function deleteSelectedMembers() {
    const selectedIds = new Set(
      table.getFilteredSelectedRowModel().rows.map((row) => row.original.id)
    )

    if (selectedIds.size === 0) {
      return
    }

    setTeamMembers((currentMembers) =>
      currentMembers.filter((member) => !selectedIds.has(member.id))
    )
    setRowSelection({})
  }

  const selectedCount = table.getFilteredSelectedRowModel().rows.length

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-2xl font-bold">Listagem e alocação da equipe</h1>
        <p className="text-muted-foreground">
          Gerencie membros da equipe, atribua papéis e distribua equipes/comitês.
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
              onClick={deleteSelectedMembers}
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
                    Nenhum membro encontrado.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        <div className="flex flex-col gap-2 pt-4 md:flex-row md:items-center md:justify-between">
          <p className="text-sm text-muted-foreground">
            {selectedCount} de {table.getFilteredRowModel().rows.length} membro(s) selecionado(s).
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