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
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

type RoleRecord = {
  id: string
  name: string
  description: string
  permissions: string[]
}

const permissionOptions = [
  "View dashboard",
  "Manage participants",
  "Manage teams",
  "Manage committees",
  "Manage docs",
  "Manage session",
]

const initialRoles: RoleRecord[] = [
  {
    id: "role-1",
    name: "Secretary General",
    description: "Top-level conference administration and oversight.",
    permissions: [
      "View dashboard",
      "Manage participants",
      "Manage teams",
      "Manage committees",
      "Manage docs",
      "Manage session",
    ],
  },
  {
    id: "role-2",
    name: "Director",
    description: "Committee leadership and operational setup.",
    permissions: ["View dashboard", "Manage participants", "Manage committees", "Manage session"],
  },
  {
    id: "role-3",
    name: "Moderator",
    description: "Debate moderation and speaking flow support.",
    permissions: ["View dashboard", "Manage session"],
  },
  {
    id: "role-4",
    name: "Press Team",
    description: "Media coverage, announcements, and internal reporting.",
    permissions: ["View dashboard", "Manage docs"],
  },
]

function PermissionBadges({ permissions }: { permissions: string[] }) {
  return (
    <div className="flex flex-wrap gap-1">
      {permissions.map((permission) => (
        <Badge key={permission} variant="secondary">
          {permission}
        </Badge>
      ))}
    </div>
  )
}

function PermissionSelector({
  permissions,
  onChange,
}: {
  permissions: string[]
  onChange: (permissions: string[]) => void
}) {
  const [open, setOpen] = React.useState(false)
  const [query, setQuery] = React.useState("")

  const visiblePermissions = React.useMemo(
    () =>
      permissionOptions.filter((permission) =>
        permission.toLowerCase().includes(query.trim().toLowerCase())
      ),
    [query]
  )

  function togglePermission(permission: string) {
    const nextPermissions = permissions.includes(permission)
      ? permissions.filter((item) => item !== permission)
      : [...permissions, permission]

    onChange(nextPermissions)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className="h-auto min-h-9 w-full justify-between gap-3 px-3 py-2"
        >
          <span className="truncate text-left">
            {permissions.length > 0 ? `${permissions.length} permission(s) selected` : "Select permissions"}
          </span>
          <ChevronDown className="size-4 shrink-0 text-muted-foreground" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <div className="border-b border-border p-2.5">
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search permissions..."
          />
        </div>
        <div className="max-h-64 overflow-y-auto p-2">
          {visiblePermissions.length > 0 ? (
            <div className="space-y-1">
              {visiblePermissions.map((permission) => {
                const isSelected = permissions.includes(permission)

                return (
                  <button
                    key={permission}
                    type="button"
                    onClick={() => togglePermission(permission)}
                    className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-left text-sm hover:bg-muted"
                  >
                    <Checkbox checked={isSelected} aria-hidden="true" />
                    <span className="flex-1">{permission}</span>
                  </button>
                )
              })}
            </div>
          ) : (
            <p className="px-2 py-4 text-center text-sm text-muted-foreground">No permissions found.</p>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}

export default function ManagePermsRoles() {
  const [roles, setRoles] = React.useState<RoleRecord[]>(initialRoles)
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})

  const updatePermissions = React.useCallback((id: string, permissions: string[]) => {
    setRoles((currentRoles) =>
      currentRoles.map((role) => (role.id === id ? { ...role, permissions } : role))
    )
  }, [])

  const columns = React.useMemo<ColumnDef<RoleRecord>[]>(
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
            aria-label="Select all"
          />
        ),
        cell: ({ row }) => (
          <Checkbox
            checked={row.getIsSelected()}
            onCheckedChange={(value) => row.toggleSelected(!!value)}
            aria-label="Select row"
          />
        ),
        enableSorting: false,
        enableHiding: false,
      },
      {
        accessorKey: "name",
        header: ({ column }) => (
          <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc") }>
            Role
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
      },
      {
        accessorKey: "description",
        header: ({ column }) => (
          <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc") }>
            Description
            <ArrowUpDown className="ml-2" />
          </Button>
        ),
        cell: ({ row }) => <span className="text-muted-foreground">{row.original.description}</span>,
      },
      {
        accessorKey: "permissions",
        header: "Permissions",
        cell: ({ row }) => (
          <div className="space-y-3">
            <PermissionSelector
              permissions={row.original.permissions}
              onChange={(nextPermissions) => updatePermissions(row.original.id, nextPermissions)}
            />
            <PermissionBadges permissions={row.original.permissions} />
          </div>
        ),
      },
    ],
    [updatePermissions]
  )

  // eslint-disable-next-line react-hooks/incompatible-library -- React Compiler is not enabled; TanStack Table's mutable table API is intentional.
  const table = useReactTable({
    data: roles,
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

  function deleteSelectedRoles() {
    const selectedIds = new Set(
      table.getFilteredSelectedRowModel().rows.map((row) => row.original.id)
    )

    if (selectedIds.size === 0) {
      return
    }

    setRoles((currentRoles) => currentRoles.filter((role) => !selectedIds.has(role.id)))
    setRowSelection({})
  }

  const selectedCount = table.getFilteredSelectedRowModel().rows.length

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-2xl font-bold">Roles and permissions</h1>
        <p className="text-muted-foreground">
          Review roles and toggle the permissions granted to each role.
        </p>
      </div>

      <div className="rounded-3xl border border-border bg-background p-4 shadow-sm">
        <div className="flex flex-col gap-3 pb-4 md:flex-row md:items-center">
          <Input
            placeholder="Search by role name..."
            value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
            onChange={(event) => table.getColumn("name")?.setFilterValue(event.target.value)}
            className="w-full md:max-w-sm"
          />

          <div className="flex flex-wrap items-center gap-2 md:ml-auto">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">
                  Columns
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

            <Button variant="destructive" onClick={deleteSelectedRoles} disabled={selectedCount === 0}>
              Delete selected
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
                        : flexRender(header.column.columnDef.header, header.getContext())}
                    </TableHead>
                  ))}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows.length > 0 ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow key={row.id} data-state={row.getIsSelected() ? "selected" : undefined}>
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
                    No roles found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        <div className="flex flex-col gap-2 pt-4 md:flex-row md:items-center md:justify-between">
          <p className="text-sm text-muted-foreground">
            {selectedCount} of {table.getFilteredRowModel().rows.length} role(s) selected.
          </p>

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
              Previous
            </Button>
            <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
              Next
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
