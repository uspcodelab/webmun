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
import { ArrowUpDown, ChevronDown, PlusIcon } from "lucide-react"

import { useConference } from "@/context/ConferenceContext"
import type { CommitteeRead } from "@/schemas/types.gen"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

function formatDate(value: string) {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value))
}

export default function CommitteeManagement() {
  const {
    activeConference,
    committees,
    createCommittee,
    loading,
    error,
    canManageConference,
  } = useConference()
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false)
  const [committeeName, setCommitteeName] = React.useState("")
  const [submitError, setSubmitError] = React.useState<string | null>(null)
  const [submitting, setSubmitting] = React.useState(false)

  async function handleCreateCommittee(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedName = committeeName.trim()
    if (!trimmedName) {
      return
    }

    setSubmitting(true)
    setSubmitError(null)

    try {
      await createCommittee({ name: trimmedName })
      setCommitteeName("")
      setCreateDialogOpen(false)
    } catch (createError) {
      setSubmitError(
        createError instanceof Error ? createError.message : "Failed to create committee"
      )
    } finally {
      setSubmitting(false)
    }
  }

  const columns = React.useMemo<ColumnDef<CommitteeRead>[]>(
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
            aria-label="Selecionar comitê"
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
        cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
      },
      {
        accessorKey: "status",
        header: "Status",
        cell: ({ row }) => <Badge variant="secondary">{row.original.status}</Badge>,
      },
      {
        accessorKey: "created_at",
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Criado em
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {formatDate(row.original.created_at)}
          </span>
        ),
      },
      {
        id: "actions",
        header: "Ações",
        cell: () => (
          <Button variant="outline" size="sm" disabled>
            Editar
          </Button>
        ),
      },
    ],
    []
  )

  // eslint-disable-next-line react-hooks/incompatible-library -- React Compiler is not enabled; TanStack Table's mutable table API is intentional.
  const table = useReactTable({
    data: committees,
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

  const selectedCount = table.getFilteredSelectedRowModel().rows.length
  const canCreateCommittee = Boolean(activeConference && canManageConference)

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-2xl font-bold">Gestão de comitês</h1>
        <p className="text-muted-foreground">
          {activeConference
            ? `Comitês de ${activeConference.name}.`
            : "Selecione ou crie uma conferência para gerenciar comitês."}
        </p>
      </div>

      {error ? (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      ) : null}

      <div className="rounded-lg border border-border bg-background p-4 shadow-sm">
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

            <Button variant="destructive" disabled>
              Excluir selecionados
            </Button>

            <Button
              onClick={() => setCreateDialogOpen(true)}
              disabled={!canCreateCommittee}
            >
              <PlusIcon className="mr-2" />
              Criar comitê
            </Button>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border">
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
                    {loading ? "Carregando comitês..." : "Nenhum comitê encontrado."}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        <div className="flex flex-col gap-2 pt-4 md:flex-row md:items-center md:justify-between">
          <p className="text-sm text-muted-foreground">
            {selectedCount} de {table.getFilteredRowModel().rows.length} comitê(s) selecionado(s).
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

      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Criar comitê</DialogTitle>
            <DialogDescription>
              O backend atual persiste apenas o nome do comitê. Campos visuais ficam para um endpoint posterior.
            </DialogDescription>
          </DialogHeader>
          <form className="grid gap-4" onSubmit={handleCreateCommittee}>
            <div className="grid gap-2">
              <Label htmlFor="committee-name">Nome</Label>
              <Input
                id="committee-name"
                value={committeeName}
                onChange={(event) => setCommitteeName(event.target.value)}
                required
              />
            </div>
            {submitError ? (
              <p className="text-sm text-destructive">{submitError}</p>
            ) : null}
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setCreateDialogOpen(false)}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={submitting || !committeeName.trim()}>
                {submitting ? "Criando..." : "Criar"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
