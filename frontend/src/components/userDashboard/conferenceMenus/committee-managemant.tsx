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

type Committee = {
  id: string
  name: string
  logo: string
  colour: string
  acronym: string
  type: string
}

type CommitteeDraft = Omit<Committee, "id">

const committeeTypes = [
  "Traditional",
  "WIMUN",
  "Consensus",
  "Teatro de Operações",
  "Crisis",
  "Specialized",
]

function createLogoDataUrl(acronym: string, colour: string) {
  const safeAcronym = acronym.trim() || "CM"
  const safeColour = colour || "#64748b"

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="32" fill="${safeColour}" />
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#ffffff">${safeAcronym}</text>
    </svg>`
  )}`
}

const initialCommittees: Committee[] = [
  {
    id: "c4c5f1d6-0f6e-41ed-a610-52e2cbb1b54a",
    name: "Security Council",
    logo: "SC",
    colour: "#1d4ed8",
    acronym: "SC",
    type: "Traditional",
  },
  {
    id: "7f0a82f5-ae0b-4f5d-9c2c-7d2f72cbda0e",
    name: "United Nations Children’s Fund",
    logo: "UNICEF",
    colour: "#0f766e",
    acronym: "UNICEF",
    type: "WIMUN",
  },
  {
    id: "86e0f1d0-6d76-4b70-86ec-061d4e8e4f57",
    name: "World Health Organization",
    logo: "WHO",
    colour: "#15803d",
    acronym: "WHO",
    type: "Consensus",
  },
  {
    id: "bb64d5ce-0d34-4e8a-8c22-5f0b4db7ff90",
    name: "Crisis Room",
    logo: "CR",
    colour: "#b45309",
    acronym: "CR",
    type: "Teatro de Operações",
  },
]

function CommitteeLogoPreview({ logo, colour }: { logo: string; colour: string }) {
  const displayLabel = logo.trim() || "--"
  const isImageLogo = logo.startsWith("data:image/") || logo.startsWith("blob:") || /^https?:\/\//.test(logo)

  return (
    <div className="flex size-10 items-center justify-center overflow-hidden rounded-full border border-border bg-muted shadow-sm">
      {isImageLogo ? (
        <img src={logo} alt={displayLabel} className="size-full object-cover" />
      ) : (
        <div
          className="flex size-full items-center justify-center text-xs font-semibold text-white"
          style={{ backgroundColor: colour || "#64748b" }}
          title={logo}
          aria-label={`Logo ${displayLabel}`}
        >
          {displayLabel}
        </div>
      )}
    </div>
  )
}

export default function CommitteeManagement() {
  const [committees, setCommittees] = React.useState<Committee[]>(initialCommittees)
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})
  const [editingCommitteeId, setEditingCommitteeId] = React.useState<string | null>(null)
  const [draftCommittee, setDraftCommittee] = React.useState<CommitteeDraft | null>(null)

  const editingCommittee = React.useMemo(
    () => committees.find((committee) => committee.id === editingCommitteeId) ?? null,
    [committees, editingCommitteeId]
  )

  React.useEffect(() => {
    if (!editingCommittee) {
      setDraftCommittee(null)
      return
    }

    setDraftCommittee({
      name: editingCommittee.name,
      logo: editingCommittee.logo,
      colour: editingCommittee.colour,
      acronym: editingCommittee.acronym,
      type: editingCommittee.type,
    })
  }, [editingCommittee])

  function openEditor(id: string) {
    setEditingCommitteeId(id)
  }

  function closeEditor() {
    setEditingCommitteeId(null)
  }

  async function handleLogoFileChange(file: File | null) {
    if (!file) {
      return
    }

    const nextLogo = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader()

      reader.onload = () => resolve(String(reader.result ?? ""))
      reader.onerror = () => reject(reader.error)
      reader.readAsDataURL(file)
    })

    setDraftCommittee((currentDraft) =>
      currentDraft ? { ...currentDraft, logo: nextLogo } : currentDraft
    )
  }

  function saveDraftCommittee() {
    if (!editingCommittee || !draftCommittee) {
      return
    }

    setCommittees((currentCommittees) =>
      currentCommittees.map((committee) =>
        committee.id === editingCommittee.id
          ? {
              ...committee,
              ...draftCommittee,
              logo:
                draftCommittee.logo ||
                createLogoDataUrl(draftCommittee.acronym, draftCommittee.colour),
            }
          : committee
      )
    )
    closeEditor()
  }

  const columns = React.useMemo<ColumnDef<Committee>[]>(
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
        accessorKey: "logo",
        header: "Logo",
        cell: ({ row }) => (
          <div className="flex items-center gap-3">
            <CommitteeLogoPreview logo={row.original.logo} colour={row.original.colour} />
            <span className="text-sm text-muted-foreground">Imagem do comitê</span>
          </div>
        ),
      },
      {
        accessorKey: "colour",
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Cor
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => (
          <div className="flex items-center gap-3">
            <span
              className="size-6 rounded-full border border-border"
              style={{ backgroundColor: row.original.colour }}
              aria-hidden="true"
            />
            <span className="font-mono text-sm">{row.original.colour}</span>
          </div>
        ),
      },
      {
        accessorKey: "acronym",
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Acrônimo
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => <span className="uppercase">{row.original.acronym}</span>,
      },
      {
        accessorKey: "type",
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Tipo
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => <span>{row.original.type}</span>,
      },
      {
        id: "actions",
        header: "Ações",
        cell: ({ row }) => (
          <Button variant="outline" size="sm" onClick={() => openEditor(row.original.id)}>
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

  function deleteSelectedCommittees() {
    const selectedIds = new Set(
      table.getFilteredSelectedRowModel().rows.map((row) => row.original.id)
    )

    if (selectedIds.size === 0) {
      return
    }

    setCommittees((currentCommittees) =>
      currentCommittees.filter((committee) => !selectedIds.has(committee.id))
    )
    setRowSelection({})
  }

  const selectedCount = table.getFilteredSelectedRowModel().rows.length

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-2xl font-bold">Gestão de comitês</h1>
        <p className="text-muted-foreground">
          Edite nome, logo, cor, acrônimo e tipo dos comitês da conferência.
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
              onClick={deleteSelectedCommittees}
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
                    Nenhum comitê encontrado.
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

      <Dialog open={Boolean(editingCommitteeId)} onOpenChange={(open) => !open && closeEditor()}>
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>Editar comitê</DialogTitle>
            <DialogDescription>
              Atualize os atributos do comitê no formulário. O logo é enviado como arquivo de imagem.
            </DialogDescription>
          </DialogHeader>

          {draftCommittee ? (
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="grid gap-2 sm:col-span-2">
                <Label htmlFor="committee-name">Nome</Label>
                <Input
                  id="committee-name"
                  value={draftCommittee.name}
                  onChange={(event) =>
                    setDraftCommittee((currentDraft) =>
                      currentDraft ? { ...currentDraft, name: event.target.value } : currentDraft
                    )
                  }
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="committee-acronym">Acrônimo</Label>
                <Input
                  id="committee-acronym"
                  value={draftCommittee.acronym}
                  onChange={(event) =>
                    setDraftCommittee((currentDraft) =>
                      currentDraft
                        ? { ...currentDraft, acronym: event.target.value.toUpperCase() }
                        : currentDraft
                    )
                  }
                  className="uppercase"
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="committee-type">Tipo</Label>
                <Select
                  value={draftCommittee.type}
                  onValueChange={(value) =>
                    setDraftCommittee((currentDraft) =>
                      currentDraft ? { ...currentDraft, type: value } : currentDraft
                    )
                  }
                >
                  <SelectTrigger id="committee-type">
                    <SelectValue placeholder="Selecionar tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {committeeTypes.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid gap-2">
                <Label htmlFor="committee-colour">Cor</Label>
                <Input
                  id="committee-colour"
                  type="color"
                  value={draftCommittee.colour}
                  onChange={(event) =>
                    setDraftCommittee((currentDraft) =>
                      currentDraft ? { ...currentDraft, colour: event.target.value } : currentDraft
                    )
                  }
                  className="h-10 w-full p-1"
                />
              </div>

              <div className="grid gap-2 sm:col-span-2">
                <Label htmlFor="committee-logo">Logo</Label>
                <div className="flex flex-col gap-3 rounded-xl border border-border p-3 sm:flex-row sm:items-center">
                  <CommitteeLogoPreview logo={draftCommittee.logo} colour={draftCommittee.colour} />
                  <div className="grid gap-2 sm:flex-1">
                    <Input
                      id="committee-logo"
                      type="file"
                      accept="image/*"
                      onChange={(event) => {
                        void handleLogoFileChange(event.target.files?.[0] ?? null)
                      }}
                    />
                    <p className="text-xs text-muted-foreground">
                      Se você escolher um novo arquivo, ele substituirá o logo atual.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : null}

          <DialogFooter>
            <Button variant="outline" onClick={closeEditor}>
              Cancelar
            </Button>
            <Button onClick={saveDraftCommittee}>Salvar alterações</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
