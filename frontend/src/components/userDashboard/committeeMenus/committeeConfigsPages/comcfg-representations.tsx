import * as React from "react"
import { PlusIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@/components/ui/combobox"
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

// Placeholder data until this is wired to the backend.
const availableCountries = [
  "Brasil",
  "Argentina",
  "Estados Unidos",
  "França",
  "Alemanha",
  "Japão",
  "China",
  "Índia",
  "Nigéria",
  "África do Sul",
]

const availableUsers = ["Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Alves"]

const UNASSIGNED = "unassigned"

type Representation = { country: string; user: string }

export default function CommitteeRepresentations() {
  const [representations, setRepresentations] = React.useState<Representation[]>([
    { country: "Brasil", user: UNASSIGNED },
    { country: "França", user: UNASSIGNED },
  ])
  const [selectedCountry, setSelectedCountry] = React.useState<string | null>(null)

  const addableCountries = availableCountries.filter(
    (country) => !representations.some((item) => item.country === country)
  )

  function assignUser(country: string, user: string) {
    setRepresentations((current) =>
      current.map((item) => (item.country === country ? { ...item, user } : item))
    )
  }

  function addRepresentation() {
    if (!selectedCountry) return
    setRepresentations((current) => [
      ...current,
      { country: selectedCountry, user: UNASSIGNED },
    ])
    setSelectedCountry(null)
  }

  return (
    <div className="flex w-full flex-col gap-4">
      <div className="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>País</TableHead>
              <TableHead>Usuário alocado</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {representations.length > 0 ? (
              representations.map((item) => (
                <TableRow key={item.country}>
                  <TableCell className="font-medium">{item.country}</TableCell>
                  <TableCell>
                    <Select
                      value={item.user}
                      onValueChange={(user) => assignUser(item.country, user)}
                    >
                      <SelectTrigger className="w-56">
                        <SelectValue placeholder="Selecionar usuário" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value={UNASSIGNED}>Não alocado</SelectItem>
                        {availableUsers.map((user) => (
                          <SelectItem key={user} value={user}>
                            {user}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={2} className="h-24 text-center">
                  Nenhuma representação adicionada.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center gap-2">
        <Combobox
          items={addableCountries}
          value={selectedCountry}
          onValueChange={setSelectedCountry}
        >
          <ComboboxInput placeholder="Selecionar país..." className="w-64" />
          <ComboboxContent>
            <ComboboxEmpty>Nenhum país encontrado.</ComboboxEmpty>
            <ComboboxList>
              {(country: string) => (
                <ComboboxItem key={country} value={country}>
                  {country}
                </ComboboxItem>
              )}
            </ComboboxList>
          </ComboboxContent>
        </Combobox>
        <Button onClick={addRepresentation} disabled={!selectedCountry}>
          <PlusIcon className="mr-2" />
          Adicionar representação
        </Button>
      </div>
    </div>
  )
}
